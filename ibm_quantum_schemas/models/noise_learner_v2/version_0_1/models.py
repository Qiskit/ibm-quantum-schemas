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

from typing import Literal

from pydantic import BaseModel, Field

from ...base_params_model import BaseParamsModel


class RuntimeEncodedCircuitModel(BaseModel):
    """A circuit encoded by RuntimeEncoder.
    
    RuntimeEncoder wraps QPY-encoded circuits in a dict with __type__ and __value__ fields.
    """

    type_: Literal["QuantumCircuit"] = Field(alias="__type__")
    """The type marker used by RuntimeEncoder."""

    value: str = Field(alias="__value__")
    """Base64-encoded QPY serialization of the quantum circuit."""


class ParamsModel(BaseParamsModel):
    """A model describing the NoiseLearnerV2 program inputs also known as "params"."""

    schema_version: str = "v0.1"

    circuits: list[RuntimeEncodedCircuitModel]
    """The circuits to run the noise learner program for.
    
    Each circuit is QPY-encoded and wrapped in RuntimeEncoder format. Note that while
    the noise learner accepts EstimatorPubLike objects, they are converted to circuits
    before serialization, so only circuits appear in the serialized params.
    """

    options: "OptionsModel"
    """Options for the noise learner runtime."""


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

