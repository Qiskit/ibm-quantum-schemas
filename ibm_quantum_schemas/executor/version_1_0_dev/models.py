# This code is a Qiskit project.
#
# (C) Copyright IBM 2026.
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
from typing import Annotated, Literal

from pydantic import BaseModel, Field, JsonValue, field_validator, model_validator
from qiskit import QuantumCircuit
from typing_extensions import TypeAliasType

from ibm_quantum_schemas.aliases import Self
from ibm_quantum_schemas.common import (
    BaseParamsModel,
    F64TensorModel,
    PauliLindbladMapModel,
    QpyDataV13ToV17Model,
    TensorModel,
)
from ibm_quantum_schemas.common import SamplexModelSSV1ToSSV3 as SamplexModel

# TypeAliasType is required for Pydantic to handle this recursive type correctly.
# Note that TypeAliasType is a backport for Python<3.12, so that when drop Python 3.11 support and
# lower, this can be updated to `type DataTree = ...`.
# TensorModel must come before dict so Pydantic tries it first during deserialization.
DataTree = TypeAliasType(
    "DataTree",
    list["DataTree"] | TensorModel | dict[str, "DataTree"] | str | float | int | bool | None,
)
"""Arbitrary nesting of lists and dicts with typed leaves."""


class ParamsModel(BaseParamsModel):
    """A model describing the Executor program inputs."""

    schema_version: Literal["v1.0"] = "v1.0"

    quantum_program: QuantumProgramModel
    """The quantum program to execution."""

    options: OptionsModel
    """Options for runtime."""


class OptionsModel(BaseModel):
    """Runtime options."""

    init_qubits: bool = True
    r"""Whether to reset the qubits to the ground state for each shot."""

    rep_delay: float | None = None
    r"""The repetition delay.

    This is the delay between the end of one circuit and the start of the next within a shot loop.
    This is only supported on backends that have ``backend.dynamic_reprate_enabled=True``. It must
    be from the range supplied by ``backend.rep_delay_range``. When this value is ``None``, the
    default value ``backend.default_rep_delay`` is used.
    """

    scheduler_timing: bool = False
    """Whether to return circuit schedule timing of each provided quantum circuit.

    Setting this value to true will cause corresponding metadata of every program item to be
    populated in the returned data.
    """

    stretch_values: bool = False
    """Whether to return numeric resolutions of stretches for each provided quantum circuit.

    Setting this value to true will cause corresponding metadata of every program item to be
    populated in the returned data.
    """

    experimental: dict[str, JsonValue] = Field(default_factory=dict)
    """Experimental options.

    These options are not guaranteed to be stable and may change or be removed without notice.
    """


class CircuitItemModel(BaseModel):
    """Execution specifications for a single quantum circuit.

    The circuit for each item is store separately in ``QuantumProgramModel``.
    """

    item_type: Literal["circuit"] = "circuit"
    """The type of quantum program item."""

    circuit_arguments: F64TensorModel
    """Arguments to the parameters of the circuit.

    The last axis is over ``circuit.parameters``. Execution broadcasts over the
    preceding axes; expect one result per element of the leading shape.
    """

    shape: list[int]
    """The shape of this item.

    This shape must extend (via broadcasting) the implicit shape of the :attr:~circuit_arguments`.
    The non-trivial axes it introduces represent replications.
    """

    chunk_size: Annotated[int, Field(ge=1)] | Literal["auto"] = "auto"
    """The maximum number circuit arguments to bind to the circuit per shot loop.

    When ``"auto"``, the number is chosen server-side with heuristics designed to optimize
    execution speed. A quantum program must have items where either all chunk sizes are
    integer-valued, or all chunk sizes are ``"auto"``. Integer values are only allowed inside of
    session exection mode.
    """


class SamplexItemModel(BaseModel):
    """Execution specifications for a single quantum circuit.

    The circuit for each item is store separately in ``QuantumProgramModel``.
    """

    item_type: Literal["samplex"] = "samplex"
    """The type of quantum program item."""

    samplex: SamplexModel
    """A JSON-encoded samplex."""

    samplex_arguments: dict[str, bool | int | PauliLindbladMapModel | TensorModel]
    """Arguments to the samplex."""

    shape: list[int]
    """The shape of this item.

    This shape must extend (via broadcasting) the implicit shape of the :attr:~samplex_arguments`.
    The non-trivial axes it introduces enumerate randomizations.
    """

    chunk_size: Annotated[int, Field(ge=1)] | Literal["auto"] = "auto"
    """The maximum number circuit arguments to bind to the circuit per shot loop.

    When ``"auto"``, the number is chosen server-side with heuristics designed to optimize
    execution speed. A quantum program must have items where either all chunk sizes are
    integer-valued, or all chunk sizes are ``"auto"``. Integer values are only allowed inside of
    session exection mode.
    """


class QuantumProgramModel(BaseModel):
    """Model to store a quantum program."""

    shots: int = Field(ge=1)
    """The number of shots for each individually bound circuit."""

    circuits: QpyDataV13ToV17Model[QuantumCircuit]
    """One quantum circuit for every element of ``items``.

    These are stored outside of ``items`` to cosituate them inside of one QPY blob.
    """

    items: list[Annotated[CircuitItemModel | SamplexItemModel, Field(discriminator="item_type")]]
    """Items of the program."""

    semantic_role: str | None = Field(default=None, examples=["sampler-v2", "estimator-v2"])
    """Semantic role indicating how execution results may be post-processed by runtime clients.

    Reserved system values include 'sampler-v2' and 'estimator-v2', and are subject to change
    without notice. Third party clients should not set or depend on this value.
    """

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

    @model_validator(mode="after")
    def check_circuit_count_is_consistent(self):
        """Check that there is one circuit for every item."""
        if self.circuits.num_programs != len(self.items):
            raise ValueError(
                "There must be exactly one circuit for every program item, but there are "
                f"{self.circuits.num_programs} circuits and {len(self.items)} items."
            )

        return self

    meas_level: Literal["classified", "kerneled", "avg_kerneled", "both"] = "classified"
    """The level at which to return all classical register measurement results.

    This option sets the return type of all classical registers in all quantum program items and
    determines whether the raw complex data from low-level measurement devices is discriminated
    into bits or not.

     - "classified": Classical register data is returned as boolean arrays with the intrinsic shape
         ``(num_shots, creg_size)``.
     - "kerneled": Classical register data is returned as a complex array with the intrinsic shape
         ``(num_shots, creg_size)``, where each entry represents an IQ data point (resulting from
         kerneling the measurement trace) in arbitrary units.
     - "avg_kerneled": Classical register data is returned as a complex array with the intrinsic
         shape ``(creg_size,)``, where data is equivalent to "kerneled" except additionally averaged
         over shots.
     - "both": Both classified and kerneled data is returned for every classical register.
    """

    passthrough_data: DataTree = None
    """Arbitrary nested data passed through execution without modification."""


class SchedulerTimingModel(BaseModel):
    """Describes the timing of a scheduled circuit.

    All timing information is expressed in terms of multiples of the quantity ``dt``, time step
    duration of the control electronics, which can be queried in backend and target properties.
    """

    timing: str
    """A description of circuit timing in a comma-separated text format."""

    circuit_duration: int
    """The duration of the circuit in ``dt`` steps."""


class StretchValueModel(BaseModel):
    """Describes circuit stretch value resolutions.

    All timing information is expressed in terms of multiples of the quantity ``dt``, time step
    duration of the control electronics, which can be queried in backend and target properties.
    """

    name: str
    """The name of the stretch."""

    value: int
    """The resolved stretch value, up to the remainder, in units of ``dt``."""

    remainder: int
    """The time left over if ``value`` were to be used each stretch, in units of ``dt``."""

    expanded_values: list[tuple[int, int]]
    """A sequence of pairs ``(time, duration)`` indicating the time and duration of each delay.

    All units are ``dt``, where the ``time`` denotes the absolute time of a delay in the circuit
    schedule, and the ``duration`` denotes the total duration of the delay.
    """


class ItemMetadataModel(BaseModel):
    """Per-item metadata for quantum program results."""

    scheduler_timing: SchedulerTimingModel | None = None
    """Scheduled circuit timing information, if it is available."""

    stretch_values: list[StretchValueModel] | None = None
    """Stretch value resolution, if it is available."""


class QuantumProgramResultItemModel(BaseModel):
    """Results for a single quantum program item."""

    results: dict[str, TensorModel]
    """A map from results to their tensor values."""

    metadata: ItemMetadataModel
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

    permutation: list[int]
    """A permutation vector of the item shape before slicing elements with the ``element_range``.

    This list should hold contiguous integers starting at 0, in some order. The convention is
    that ``permuted_shape[i] = shape[permutation[i]]`` for every dimension index ``i``.
    """

    element_range: tuple[int, int, int]
    """Which elements of the item were executed in this chunk part.

    This range has entries ``(start_idx, stop_idx, step)`` that slice the flattened shape of the
    corresponding quantum program item, after the ``permutation`` has been applied. That is,
    this part corresponds to the data elements ``flatten(permute(arr))[start_idx:stop_idx:step]``
    for some data array ``arr`` whose shape matches the corresponding item shape. The lower index
    is inclusive, the upper index is exclusive, and the step must be positive.

    It should hold that ``size == max(0, ceil((stop_idx - start_idx) / step))``.
    """

    @field_validator("permutation", mode="after")
    @classmethod
    def must_be_permutation_of_range(cls, value):
        """Check that we have a valid permutation vector."""
        if set(value) != set(range(len(value))):
            raise ValueError(f"Must be a permutation of [0, 1, ..., {len(value) - 1}].")
        return value

    @field_validator("element_range", mode="after")
    @classmethod
    def must_be_a_valid_range(cls, value):
        """Check that we have a valid range tuple."""
        start, stop, step = value
        if start < 0 or stop < start or step < 1:
            raise ValueError("Must be a valid range.")
        return value

    @model_validator(mode="after")
    def cross_validate(self) -> Self:
        """Check for mutual compatibility of types and shapes of attributes."""
        if len(range(*self.element_range)) != self.size:
            raise ValueError(
                f"The start, stop, and step integers, {tuple(self.element_range)}, "
                f"are inconsistent with the total size, {self.size}."
            )

        return self


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

    schema_version: Literal["v1.0"] = "v1.0"
    """Schema version of the result type."""

    data: list[QuantumProgramResultItemModel]
    """Resulting data for each quantum program item."""

    metadata: MetadataModel
    """Execution metadata pertaining to the job as a whole."""

    passthrough_data: DataTree = None
    """Arbitrary nested data passed through execution without modification."""

    semantic_role: str | None = Field(default=None, examples=["sampler-v2", "estimator-v2"])
    """Semantic role indicating how execution results may be post-processed by runtime clients.

    Reserved system values include 'sampler-v2' and 'estimator-v2', and are subject to change
    without notice. Third party clients should not set or depend on this value.
    """
