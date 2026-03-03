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

from ...base_params_model import BaseParamsModel
from ...typed_qpy_circuit_model import TypedQpyCircuitModelV13to17
from .layer_noise_model import (
    LayerNoiseModel,
    LayerNoiseWrapperModel,
    NdarrayWrapperModel,
    PauliLindbladErrorModel,
    PauliLindbladErrorWrapperModel,
    PauliListModel,
    PauliListWrapperModel,
)
from .options_model import OptionsModel, SimulatorOptionsModel
from .results_metadata_model import InputOptionsModel, ResultsMetadataModel


class ParamsModel(BaseParamsModel):
    """A model describing the NoiseLearnerV2 program inputs, also known as "params"."""

    model_config = ConfigDict(extra="forbid")

    schema_version: str = "v0.1"
    """Schema version of the program input."""

    version: Literal[2] | None = 2
    """Version of the program."""

    circuits: list[TypedQpyCircuitModelV13to17 | str]
    """The circuits to run the noise learner program for.

    The list may contain individual circuits serialized in one of the following ways:
    - QPY format (Packaged in `TypedQpyCircuitModelV13to17`)
    - QASM string (stored directly as a `str` in the list)
    """

    options: OptionsModel = OptionsModel()
    """Options for the noise learner program."""


class ResultsModel(BaseModel):
    """A model describing the result from executing a noise learner v2 job."""

    schema_version: Literal["v0.1"] = "v0.1"
    """Schema version of the results."""

    data: list[LayerNoiseWrapperModel]
    """Result data from the noise learner v2 job."""

    metadata: ResultsMetadataModel
    """Metadata for the noise learner v2 job."""


__all__ = [
    "ParamsModel",
    "ResultsModel",
    "OptionsModel",
    "SimulatorOptionsModel",
    "LayerNoiseModel",
    "LayerNoiseWrapperModel",
    "NdarrayWrapperModel",
    "PauliLindbladErrorModel",
    "PauliLindbladErrorWrapperModel",
    "PauliListModel",
    "PauliListWrapperModel",
    "InputOptionsModel",
    "ResultsMetadataModel",
]
