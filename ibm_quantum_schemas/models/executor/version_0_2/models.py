# This code is a Qiskit project.
#
# (C) Copyright IBM 2025.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Models"""

from __future__ import annotations

import datetime
from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, Field, field_validator, model_validator

from ....aliases import Self
from ...base_params_model import BaseParamsModel
from ...pauli_lindblad_map_model import PauliLindbladMapModel
from ...qpy_model import QpyModelV13ToV17
from ...samplex_model import SamplexModelSSV1 as SamplexModel
from ...tensor_model import F64TensorModel, TensorModel


class ParamsModel(BaseParamsModel):
    """Schema version 2 of the inner parameters."""

    schema_version: Literal["v0.2"] = "v0.2"

    quantum_program: QuantumProgramModel
    """The quantum program to execution."""

    options: OptionsModel
    """Options for runtime."""


class OptionsModel(BaseModel):
    """Runtime options."""

    init_qubits: bool = True
    r"""Whether to reset the qubits to the ground state for each shot.
    """

    rep_delay: Optional[float] = None
    r"""The repetition delay. This is the delay between a measurement and
    the subsequent quantum circuit. This is only supported on backends that have
    ``backend.dynamic_reprate_enabled=True``. It must be from the
    range supplied by ``backend.rep_delay_range``.
    Default is given by ``backend.default_rep_delay``.
    """


class CircuitItemModel(BaseModel):
    """Execution specifications for a single quantum circuit."""

    item_type: Literal["circuit"] = "circuit"
    """The type of quantum program item."""

    circuit: QpyModelV13ToV17
    """A QPY-encoded circuit."""

    circuit_arguments: F64TensorModel
    """Arguments to the parameters of the circuit.

    The last axis is over ``circuit.parameters``. Execution broadcasts over the
    preceding axes; expect one result per element of the leading shape.
    """

    chunk_size: Union[Annotated[int, Field(ge=1)], Literal["auto"]] = "auto"
    """The maximum number circuit arguments to bind to the circuit per shot loop.

    When ``"auto"``, the number is chosen server-side with heuristics designed to optimize
    execution speed. A quantum program must have items where either all chunk sizes are
    integer-valued, or all chunk sizes are ``"auto"``. Integer values are only allowed inside of
    session exection mode.
    """

    @model_validator(mode="after")
    def cross_validate(self) -> Self:
        """Check for mutual compatibility of types and shapes of attributes."""
        circuit = self.circuit.to_quantum_circuit(use_cached=True)

        num_parameters = self.circuit_arguments.shape[-1] if self.circuit_arguments.shape else 0
        if num_parameters != circuit.num_parameters:
            raise ValueError(
                f"The size of the last axis of circuit arguments, {num_parameters}, does not "
                f"match the number of parameters of the circuit, {circuit.num_parameters}."
            )

        return self


class SamplexItemModel(BaseModel):
    """Execution specifications for a single quantum circuit."""

    item_type: Literal["samplex"] = "samplex"
    """The type of quantum program item."""

    circuit: QpyModelV13ToV17
    """A QPY-encoded circuit."""

    samplex: SamplexModel
    """A JSON-encoded samplex."""

    samplex_arguments: dict[str, Union[bool, int, PauliLindbladMapModel, TensorModel]]
    """Arguments to the samplex."""

    shape: list[int]
    """The shape of this item.

    This shape must extend (via broadcasting) the implicit shape of the :attr:~samplex_arguments`.
    The non-trivial axes it introduces enumerate randomizations.
    """

    chunk_size: Union[Annotated[int, Field(ge=1)], Literal["auto"]] = "auto"
    """The maximum number circuit arguments to bind to the circuit per shot loop.

    When ``"auto"``, the number is chosen server-side with heuristics designed to optimize
    execution speed. A quantum program must have items where either all chunk sizes are
    integer-valued, or all chunk sizes are ``"auto"``. Integer values are only allowed inside of
    session exection mode.
    """

    @model_validator(mode="after")
    def cross_validate(self) -> Self:
        """Check for mutual compatibility of types and shapes of attributes."""
        circuit = self.circuit.to_quantum_circuit(use_cached=True)
        samplex = self.samplex.to_samplex(use_cached=True)

        if specs := samplex.outputs().get_specs("parameter_values"):
            num_output_params = specs[0].shape[-1]
        else:
            num_output_params = 0
        if (num_samplex_out := num_output_params) != circuit.num_parameters:
            raise ValueError(
                f"The number of samplex output parameters, {num_samplex_out}, does not match the "
                f"number of parameters of the circuit, {circuit.num_parameters}."
            )

        return self


class QuantumProgramModel(BaseModel):
    """Model to store a quantum program."""

    shots: int = Field(ge=1)
    """The number of shots for each individually bound circuit."""

    items: list[
        Annotated[Union[CircuitItemModel, SamplexItemModel], Field(discriminator="item_type")]
    ]
    """Items of the program."""

    @model_validator(mode="after")
    def check_chunk_sizes_are_consistent(self):
        """Check that all program items set chunk sizes consistently."""
        chunk_sizes = {item.chunk_size for item in self.items}
        if "auto" in chunk_sizes and len(chunk_sizes) > 1:
            raise ValueError(
                "Some quantum program items specified an integer-valued 'chunk_size' while others "
                "specified 'auto', but all items must specify one or the other."
            )

        return self


class QuantumProgramResultItemModel(BaseModel):
    """Results for a single quantum program item."""

    results: dict[str, TensorModel]
    """A map from results to their tensor values."""

    metadata: None
    """Metadata pertaining to the execution of this particular quantum program item."""


class ChunkPart(BaseModel):
    """A description of the contents of a single part of an execution chunk."""

    idx_item: int
    """The index of an item in a quantum program."""

    size: int
    """The number of elements from the quantum program item that were executed.

    For example, if a quantum program item has shape ``(10, 5)``, then it has a total of ``50``
    elements, so that if this ``size`` is ``10``, it constitutes 20% of the total work for the item.
    """


class ChunkSpan(BaseModel):
    """Timing information about a single chunk of execution.

    .. note::

        This span may include some amount of non-circuit time.
    """

    start: datetime.datetime
    """The start time of the execution chunk in UTC."""

    stop: datetime.datetime
    """The stop time of the execution chunk in UTC."""

    parts: list[ChunkPart]
    """A description of which parts of a quantum program are contained in this chunk."""


class MetadataModel(BaseModel):
    """Execution metadata."""

    chunk_timing: list[ChunkSpan]
    """Timing information about all executed chunks of a quantum program."""


class QuantumProgramResultModel(BaseModel):
    """Result from executing a quantum program."""

    schema_version: Literal["v0.2"] = "v0.2"
    """Schema version of the result type."""

    data: list[QuantumProgramResultItemModel]
    """Resulting data for each quantum program item."""

    metadata: MetadataModel
    """Execution metadata pertaining to the job as a whole."""

    @field_validator("metadata", mode="before")
    @classmethod
    def upgrade_none_to_metadata(cls, value):
        """Upgrade none values to empty metadata."""
        # this is to account for an older version of v0.2, before its release, where metadata was
        # temporarily set to None
        if value is None:
            value = MetadataModel(chunk_timing=[])
        return value
