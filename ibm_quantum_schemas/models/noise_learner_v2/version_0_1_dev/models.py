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

"""Models for NoiseLearnerV2 inputs and outputs"""

from ...base_params_model import BaseParamsModel
from .circuit_qpy_model_v13_to_v17 import CircuitQpyModelV13to17
from .options_model import OptionsModel


class ParamsModel(BaseParamsModel):
    """A model describing the NoiseLearnerV2 program inputs, also known as "params"."""

    schema_version: str = "v0.1"

    circuits: list[CircuitQpyModelV13to17]
    """The circuits to run the noise learner program for.

    Each circuit is QPY-encoded and wrapped in RuntimeEncoder format. Note that while
    the noise learner accepts EstimatorPubLike objects, they are converted to circuits
    before serialization, so only circuits appear in the serialized params.
    """

    options: "OptionsModel"
    """Options for the noise learner runtime."""
