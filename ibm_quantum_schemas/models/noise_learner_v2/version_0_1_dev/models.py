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

import struct
import zlib
from io import BytesIO
from typing import Literal

import pybase64
from pydantic import BaseModel, Field, conlist, model_validator
from qiskit.qpy.formats import FILE_HEADER_V10, FILE_HEADER_V10_PACK, FILE_HEADER_V10_SIZE

from ...base_params_model import BaseParamsModel


class CircuitQpyModelV13to14(BaseModel):
    """A circuit representation used in some primitives."""

    type_: Literal["QuantumCircuit"] = Field(alias="__type__")
    """The type marker used by RuntimeEncoder."""

    value: str = Field(alias="__value__")
    """
    Base64-encoded string containing zlib-compressed QPY serialization of the quantum circuit.

    The qpy version should be 13 or 14.
    """

    @model_validator(mode="after")
    def validate_qpy_version(self):
        """Constrain the allowed QPY encodings to versions 13-14."""
        # Decode base64 and decompress
        compressed_data = pybase64.b64decode(self.value)
        qpy_data = zlib.decompress(compressed_data)

        # Read QPY header
        with BytesIO(qpy_data) as bytes_obj:
            header = FILE_HEADER_V10._make(
                struct.unpack(
                    FILE_HEADER_V10_PACK,
                    bytes_obj.read(FILE_HEADER_V10_SIZE),
                )
            )
            if header.qpy_version < 13 or header.qpy_version > 14:
                raise ValueError(
                    f"The qpy_version is {header.qpy_version} but this model expects the version"
                    + "to be between 13 and 14."
                )
            if header.num_programs != 1:
                raise ValueError(
                    f"Expected exactly one encoded quantum circuit, received {header.num_programs}"
                )
        return self


class ParamsModel(BaseParamsModel):
    """A model describing the NoiseLearnerV2 program inputs also known as "params"."""

    schema_version: str = "v0.1"

    circuits: list[CircuitQpyModelV13to14]
    """The circuits to run the noise learner program for.

    Each circuit is QPY-encoded and wrapped in RuntimeEncoder format. Note that while
    the noise learner accepts EstimatorPubLike objects, they are converted to circuits
    before serialization, so only circuits appear in the serialized params.
    """

    options: "OptionsModel"
    """Options for the noise learner runtime."""


class SimulatorOptionsModel(BaseModel):
    """Simulator options for the noise learner."""

    noise_model: dict | None = None
    """Noise model for the simulator.

    This option is only supported in local testing mode.
    Default: ``None``.
    """

    seed_simulator: int | None = None
    """Random seed to control sampling.

    Default: ``None``.
    """

    coupling_map: conlist(conlist(int, min_length=2, max_length=2)) | None = None  # type: ignore[valid-type]
    """Directed coupling map to target in mapping.

    If the coupling map is symmetric, both directions need to be specified.
    Each entry in the list specifies a directed two-qubit interaction,
    e.g: ``[[0, 1], [0, 3], [1, 2], [1, 5], [2, 5], [4, 1], [5, 3]]``.

    Default: ``None``, which implies no connectivity constraints.
    """

    basis_gates: list[str] | None = None
    """List of basis gate names to unroll to.

    For example, ``['u1', 'u2', 'u3', 'cx']``. Unrolling is not done if not set.

    Default: all basis gates supported by the simulator.
    """


class OptionsModel(BaseModel):
    """Runtime options for the noise learner."""

    max_layers_to_learn: int | None = 4
    """The max number of unique layers to learn.

    A ``None`` value indicates that there is no limit. If there are more unique layers
    present, then some layers will not be learned or mitigated. The learned layers are
    prioritized based on the number of times they occur.
    """

    shots_per_randomization: int = 128
    """The total number of shots to use per random learning circuit.

    A learning circuit is a random circuit at a specific learning depth with a specific
    measurement basis that is executed on hardware.
    """

    num_randomizations: int = 32
    """The number of random circuits to use per learning circuit configuration.

    A configuration is a measurement basis and depth setting.
    """

    layer_pair_depths: list[int] = [0, 1, 2, 4, 16, 32]
    """The circuit depths (measured in number of pairs) to use in learning experiments.

    Pairs are used as the unit because we exploit the order-2 nature of our entangling gates
    in the noise learning implementation. For example, a value of ``3`` corresponds to 6
    repetitions of the layer of interest.
    """

    twirling_strategy: Literal["active", "active-circuit", "active-accum", "all"] = "active-accum"
    """The twirling strategy in the identified layers of two-qubit twirled gates.

    The allowed values are:

    * ``"active"``: in each individual twirled layer, only the instruction qubits are twirled.
    * ``"active-circuit"``: in each individual twirled layer, the union of all instruction
      qubits in the circuit are twirled.
    * ``"active-accum"``: in each individual twirled layer, the union of instructions qubits
      in the circuit up to the current twirled layer are twirled.
    * ``"all"``: in each individual twirled layer, all qubits in the input circuit are twirled.
    """

    support_qiskit: bool = True
    """Whether to support Qiskit-specific features."""

    experimental: dict | None = None
    """Experimental options.

    These options are subject to change without notification, and stability is not guaranteed.
    """

    simulator: SimulatorOptionsModel | None = None
    """Simulator options."""
