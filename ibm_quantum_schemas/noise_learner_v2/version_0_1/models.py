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

"""Models for NoiseLearnerV2 inputs and outputs"""

from typing import Literal

from pydantic import BaseModel, ConfigDict

from ibm_quantum_schemas.common.typed_qpy_circuit import TypedQpyCircuitModelV13to17
from ibm_quantum_schemas.noise_learner_v2.version_0_1.layer_noise import LayerNoiseWrapperModel
from ibm_quantum_schemas.noise_learner_v2.version_0_1.options import OptionsModel
from ibm_quantum_schemas.noise_learner_v2.version_0_1.results_metadata import (
    ResultsMetadataModel,
)


class ParamsModel(BaseModel):
    """A model describing the NoiseLearnerV2 program inputs, also known as "params"."""

    model_config = ConfigDict(extra="forbid")

    version: Literal[2] | None = 2
    """Version of the program."""

    circuits: list[TypedQpyCircuitModelV13to17 | str]
    """The circuits to run the noise learner program for.

    The list may contain individual circuits serialized in one of the following ways:

    * QPY format (Packaged in :class:`TypedQpyCircuitModelV13to17`)
    * QASM string (stored directly as a ``str`` in the list)
    """

    options: OptionsModel = OptionsModel()
    """Options for the noise learner program."""


class ResultsModel(BaseModel):
    """A model describing the result from executing a noise learner v2 job."""

    data: list[LayerNoiseWrapperModel]
    """Result data from the noise learner v2 job."""

    metadata: ResultsMetadataModel
    """Metadata for the noise learner v2 job."""
