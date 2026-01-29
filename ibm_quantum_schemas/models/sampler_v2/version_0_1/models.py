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

"""Models for SamplerV2 v0.1"""

from __future__ import annotations

import base64
import datetime
import io
import zlib
from typing import Annotated, Any, Literal

import numpy as np
from pydantic import BaseModel, Field, model_validator

from ....aliases import Self
from ...base_params_model import BaseParamsModel
from ...qpy_model import QpyModelV13ToV16
from ...tensor_model import F64TensorModel

# Type alias for PUB tuple format
# RuntimeEncoder encodes SamplerPub as: (circuit, parameter_values, shots)
PubModel = Annotated[
    tuple[QpyModelV13ToV16, F64TensorModel, int | None],
    Field(
        description=(
            "A Primitive Unified Bloc (PUB) as a tuple: (circuit, parameter_values, shots). "
            "The circuit is QPY-encoded, parameter_values is a tensor of parameter bindings, "
            "and shots is optional (None means use default_shots)."
        )
    ),
]


class ParamsModel(BaseParamsModel):
    """Schema version 1 of the inner parameters."""

    schema_version: Literal["v0.1"] = "v0.1"

    pubs: list[PubModel]
    """The list of PUBs for execution."""

    options: OptionsModel
    """Options for runtime."""


class DynamicalDecouplingOptionsModel(BaseModel):
    """Options for dynamical decoupling (DD)."""

    enable: bool = False
    r"""Whether to enable DD as specified by the other options in this class.

        Default: ``False``.
    """
    sequence_type: Literal["XX", "XpXm", "XY4"] = "XX"
    r"""Which dynamical decoupling sequence to use.

        Default: ``"XX"``.

        * ``"XX"``: use the sequence ``tau/2 - (+X) - tau - (+X) - tau/2``
        * ``"XpXm"``: use the sequence ``tau/2 - (+X) - tau - (-X) - tau/2``
        * ``"XY4"``: use the sequence
          ``tau/2 - (+X) - tau - (+Y) - tau (-X) - tau - (-Y) - tau/2``
    """
    extra_slack_distribution: Literal["middle", "edges"] = "middle"
    r"""Where to put extra timing delays due to rounding issues.
        Rounding issues arise because the discrete time step ``dt`` of the system cannot
        be divided. This option takes following values.

        Default: ``"middle"``.

        * ``"middle"``: Put the extra slack to the interval at the middle of the sequence.
        * ``"edges"``: Divide the extra slack as evenly as possible into intervals at
          beginning and end of the sequence.
    """
    scheduling_method: Literal["alap", "asap"] = "alap"
    r"""Whether to schedule gates as soon as ("asap") or
        as late as ("alap") possible.

        Default: ``"alap"``.
    """
    skip_reset_qubits: bool = False
    r"""Whether to insert DD on idle periods that immediately follow initialized/reset qubits.

        Since qubits in the ground state are less susceptible to decoherence, it can be beneficial
        to let them be while they are known to be in this state.

        Default: ``False``.
    """


class TwirlingOptionsModel(BaseModel):
    """Twirling options."""

    enable_gates: bool = False
    """Whether to apply 2-qubit Clifford gate twirling."""

    enable_measure: bool = False
    """Whether to enable twirling to measurement instructions, as long as the measurement is not
    involved within a conditional block."""

    num_randomizations: int | Literal["auto"] = "auto"
    r"""The number of random samples to use when twirling or peforming sampled mitigation.

    If ``num_randomizations`` is "auto", for every pub executed ``shots`` times:

      * If ``shots_per_randomization`` is also "auto", ``shots_per_randomization`` is set first
        as described below, then ``num_randomizations`` is set as
        ``ceil(shots/shots_per_randomization)``, where ``ceil`` is the ceiling function.
      * Otherwise, the value is set to ``ceil(shots/shots_per_randomization)``.

    .. note::
      The ``shots`` value specified in a PUB or in the ``run()`` method is considered part of the
      primitive execution interface and therefore is always obeyed. ``default_shots``, on the other
      hand, is considered a Qiskit Runtime specific option. Therefore, the product of
      ``num_randomizations`` and ``shots_per_randomization`` takes precedence over
      ``default_shots``.
    """

    shots_per_randomization: int | Literal["auto"] = "auto"
    r"""The number of shots to run for each random sample.

    If "auto", for every pub executed ``shots`` times:

      * If ``num_randomizations`` is also "auto", the value is set to ``64`` for PEC mitigation
        or to ``max(64, ceil(shots / 32))`` in all other cases, where ``ceil`` is the ceiling
        function.
      * Otherwise, the value is set to ``ceil(shots/num_randomizations)``.

      Default: ``"auto"``.

    .. note::
      The ``shots`` value specified in a PUB or in the ``run()`` method is considered part of the
      primitive execution interface and therefore is always obeyed. ``default_shots``, on the other
      hand, is considered a Qiskit Runtime specific option. Therefore, the product of
      ``num_randomizations`` and ``shots_per_randomization`` takes precedence over
      ``default_shots``.
    """

    strategy: Literal["active", "active-circuit", "active-accum", "all"] = "active-accum"
    r"""Specify the strategy of twirling qubits in identified layers of 2-qubit twirled gates.

      * If ``"active"`` only the instruction qubits in each individual twirled
        layer will be twirled.
      * If ``"active-circuit"`` the union of all instruction qubits in the circuit
        will be twirled in each twirled layer.
      * If ``"active-accum"`` the union of instructions qubits in the circuit up to
        the current twirled layer will be twirled in each individual twirled layer.
      * If ``"all"`` all qubits in the input circuit will be twirled in each
        twirled layer.
    """


class ExecutionOptionsModel(BaseModel):
    """Execution time options."""

    init_qubits: bool = True
    """Whether to reset the qubits to the ground state for each shot."""

    rep_delay: float | None | None = None
    r"""The repetition delay in seconds. This is the delay between the last measurement and
    the subsequent quantum circuit. This is only supported on backends that have
    ``backend.dynamic_reprate_enabled=True``. It must be from the
    range supplied by ``backend.rep_delay_range``.
    Default is given by ``backend.default_rep_delay``.
    """

    meas_type: Literal["classified", "kerneled", "avg_kerneled"] = "classified"
    r"""How to process and return measurement results.

    This option sets the return type of all classical registers in all
    :class:`~qiskit.primitives.containers.SamplerPubResult`\s.
    If a sampler pub with shape ``pub_shape`` has a circuit that contains a classical register
    with size ``creg_size``, then the returned data associated with this register will have one of
    the following formats depending on the value of this option.

    * ``"classified"``: A :class:`~qiskit.primitives.containers.BitArray` of
      shape ``pub_shape`` over ``num_shots`` with a
      number of bits equal to ``creg_size``.

    * ``"kerneled"``: A complex NumPy array of shape ``(*pub_shape, num_shots, creg_size)``, where
      each entry represents an IQ data point (resulting from kerneling the measurement trace) in
      arbitrary units.

    * ``"avg_kerneled"``: A complex NumPy array of shape ``(*pub_shape, creg_size)``, where
      each entry represents an IQ data point (resulting from kerneling the measurement trace and
      averaging over shots) in arbitrary units. This option is equivalent to selecting
      ``"kerneled"`` and then averaging over the shots axis, but requires less data bandwidth.
    """


class OptionsModel(BaseModel):
    """Runtime options.

    This matches the wire format used by qiskit-ibm-runtime and validated by
    qiskit-ibm-primitives YAML schema.
    """

    default_shots: int = 4096
    """The default number of shots to use if none are specified in a PUB
        or in the run method."""

    execution: ExecutionOptionsModel = Field(default_factory=ExecutionOptionsModel)
    """Execution time options (init_qubits, rep_delay, meas_type)."""

    dynamical_decoupling: DynamicalDecouplingOptionsModel = Field(
        default_factory=DynamicalDecouplingOptionsModel
    )
    """Dynamical decoupling options."""

    twirling: TwirlingOptionsModel = Field(default_factory=TwirlingOptionsModel)
    """Twirling options."""

    experimental: dict[str, Any] = Field(default_factory=dict)
    """Experimental options.

    Values must be JSON-serializable."""

    @model_validator(mode="after")
    def cross_validate(self) -> Self:
        """Cross validate options compatibility."""
        if self.execution.meas_type != "classified" and self.twirling.enable_measure:
            raise ValueError(
                "Kerneled measurement return and measurement twirling are not compatible. "
                "Set `.twirling.enable_measure=False` or `.execution.meas_type='classified'`"
            )
        return self


# ============================================================================
# Result Models
# ============================================================================


class BitArrayModel(BaseModel):
    """Model for BitArray data.

    BitArray stores measurement outcomes as a uint8 numpy array.
    """

    array: str
    """Base64-encoded, zlib-compressed NumPy binary data."""

    num_bits: int
    """Number of bits per shot (classical register size)."""

    @classmethod
    def from_numpy(cls, array: np.ndarray, num_bits: int) -> BitArrayModel:
        """Instantiate from a NumPy array.

        Args:
            array: A uint8 numpy array containing bit-packed measurement data.
            num_bits: Number of bits per shot (classical register size).

        Returns:
            BitArrayModel instance with encoded data.

        Raises:
            ValueError: If array is not uint8 dtype.
        """
        if array.dtype != np.uint8:
            raise ValueError(f"BitArray must be created from uint8 array, got {array.dtype}")

        with io.BytesIO() as buff:
            np.save(buff, array, allow_pickle=False)
            buff.seek(0)
            serialized_data = buff.read()

        # Compress with zlib
        compressed_data = zlib.compress(serialized_data)

        # Encode to base64 string
        encoded_string = base64.standard_b64encode(compressed_data).decode("utf-8")

        return cls(array=encoded_string, num_bits=num_bits)

    def to_numpy(self) -> np.ndarray:
        """Convert to a NumPy array.

        Returns:
            The decoded uint8 numpy array containing bit-packed measurement data.

        Raises:
            ValueError: If the data cannot be decoded or is not uint8.
        """
        try:
            # Decode from base64
            decoded = base64.standard_b64decode(self.array)

            # Decompress with zlib
            decompressed = zlib.decompress(decoded)

            # Deserialize using np.load
            with io.BytesIO(decompressed) as buff:
                array = np.load(buff, allow_pickle=False)

            # Verify it's uint8
            if array.dtype != np.uint8:
                raise ValueError(f"BitArray must contain uint8 data, got {array.dtype}")

            return array

        except Exception as e:
            raise ValueError(f"Failed to decode BitArray data: {e}") from e


class DataBinModel(BaseModel):
    """Model for DataBin data.

    DataBin is a container for measurement results, organized by classical register names.
    Each field contains a BitArray with the measurement outcomes for that register.
    """

    shape: list[int]
    """The shape of the pub (e.g., [2, 3] for a 2x3 parameter sweep)."""

    field_names: list[str]
    """List of field names in the DataBin (e.g., ["meas", "alpha"]).

    Note: This field is redundant (same as fields.keys()) but included to match
    the qiskit-ibm-runtime convention.
    """

    fields: dict[str, BitArrayModel]
    """Dictionary of measurement results.

    Keys are classical register names, values are BitArray objects containing
    the measurement outcomes for that register.
    """


class SamplerPubResultModel(BaseModel):
    """Model for SamplerPubResult data.

    Contains the measurement results (DataBin) and metadata for a single pub.
    """

    data: DataBinModel
    """The measurement results for this pub, organized by classical register."""

    metadata: dict[str, Any]
    """Circuit-specific metadata for this pub."""


class ChunkPart(BaseModel):
    """A description of the contents of a single part of an execution chunk."""

    idx_item: int
    """The index of a pub in the sampler job."""

    size: int
    """The number of elements from the pub that were executed.

    For example, if a pub has shape (10, 5), then it has a total of 50
    elements, so if this size is 10, it constitutes 20% of the total work
    for the pub.
    """


class ChunkSpan(BaseModel):
    """Timing information about a single chunk of execution.

    Note: This span may include some amount of non-circuit time.
    """

    start: datetime.datetime
    """The start time of the execution chunk in UTC."""

    stop: datetime.datetime
    """The stop time of the execution chunk in UTC."""

    parts: list[ChunkPart]
    """A description of which parts of the sampler job are contained in this chunk."""


class MetadataModel(BaseModel):
    """Execution metadata for the sampler job."""

    chunk_timing: list[ChunkSpan]
    """Timing information about all executed chunks of the sampler job."""


class SamplerResultModel(BaseModel):
    """Model for PrimitiveResult data.

    This is the top-level result object returned by the Sampler primitive.
    It contains a list of results (one per pub) and job-level metadata.

    Note: The field name is 'pub_results', not 'data'. This matches Qiskit's
    PrimitiveResult API convention.
    """

    pub_results: list[SamplerPubResultModel]
    """Resulting data for each pub in the sampler job.

    Each element corresponds to one pub submitted to the sampler, containing
    the measurement results (DataBin) and pub-specific metadata.
    """

    metadata: dict[str, Any]
    """Execution metadata pertaining to the job as a whole.

    May include timing information, backend details, and other job-level data.
    """

    @property
    def schema_version(self) -> str:
        """Schema version is implicitly v0.1 for this module."""
        return "v0.1"
