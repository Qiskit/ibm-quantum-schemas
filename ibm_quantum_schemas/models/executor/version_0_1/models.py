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

from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, Field, model_validator

from ....aliases import Self
from ...base_params_model import BaseParamsModel
from ...pauli_lindblad_map_model import PauliLindbladMapModel
from ...qpy_model import QpyModelV13ToV16
from ...samplex_model import SamplexModel
from ...tensor_model import F64TensorModel, TensorModel


class ParamsModel(BaseParamsModel):
    """Schema version 1 of the inner parameters."""

    schema_version: Literal["v0.1"] = "v0.1"

    quantum_program: QuantumProgramModel
    """The quantum program to execution."""

    options: OptionsModel
    """Options for runtime."""


class OptionsModel(BaseModel):
    """Runtime options."""

    init_qubits: bool = True
    r"""Whether to reset the qubits to the ground state for each shot.
    """

    rep_delay: Optional[float] = None  # noqa: UP045,UP007
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

    circuit: QpyModelV13ToV16
    """A QPY-encoded circuit."""

    circuit_arguments: F64TensorModel
    """Arguments to the parameters of the circuit.

    The last axis is over ``circuit.parameters``. Execution broadcasts over the
    preceding axes; expect one result per element of the leading shape.
    """

    chunk_size: int = Field(ge=1)
    """The maximum number circuit arguments to bind to the circuit per shot loop."""

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

    circuit: QpyModelV13ToV16
    """A QPY-encoded circuit."""

    samplex: SamplexModel
    """A JSON-encoded samplex."""

    samplex_arguments: dict[str, Union[bool, int, PauliLindbladMapModel, TensorModel]]  # noqa: UP007
    """Arguments to the samplex."""

    shape: list[int]
    """The shape of this item.

    This shape must extend (via broadcasting) the implicit shape of the :attr:~samplex_arguments`.
    The non-trivial axes it introduces enumerate randomizations.
    """

    chunk_size: int = Field(ge=1)
    """The maximum number circuit arguments to bind to the circuit per shot loop."""

    @model_validator(mode="after")
    def cross_validate(self) -> Self:
        """Check for mutual compatibility of types and shapes of attributes."""
        circuit = self.circuit.to_quantum_circuit(use_cached=True)
        samplex = self.samplex.to_samplex(use_cached=True)

        outputs = samplex.outputs()
        out_params = next(iter(spec for spec in outputs.specs if spec.name == "parameter_values"))
        if (num_samplex_out := out_params.shape[-1]) != circuit.num_parameters:
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
        Annotated[Union[CircuitItemModel, SamplexItemModel], Field(discriminator="item_type")]  # noqa: UP007
    ]
    """Items of the program."""


class QuantumProgramResultItemModel(BaseModel):
    """Results for a single quantum program item."""

    results: dict[str, TensorModel]
    """A map from results to their tensor values."""

    metadata: None
    """Metadata pertaining to the execution of this particular quantum program item."""


class QuantumProgramResultModel(BaseModel):
    """Result from executing a quantum program."""

    schema_version: Literal["v0.1"] = "v0.1"
    """Schema version of the result type."""

    data: list[QuantumProgramResultItemModel]
    """Resulting data for each quantum program item."""

    metadata: None
    """Execution metadata pertaining to the job as a whole."""
