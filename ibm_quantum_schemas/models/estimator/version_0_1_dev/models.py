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

from typing import Annotated, Literal

from pydantic import ConfigDict, Field

from ...base_params_model import BaseParamsModel
from .dynamical_decoupling_options_model import DynamicalDecouplingOptionsModel
from .estimator_pub_model import EstimatorPubModel
from .execution_options_model import ExecutionOptionsV2Model
from .layer_noise_learning_options_model import LayerNoiseLearningOptionsModel
from .layer_noise_model import (
    LayerNoiseModel,
    LayerNoiseWrapperModel,
    NdarrayWrapperModel,
    PauliLindbladErrorModel,
    PauliLindbladErrorWrapperModel,
    PauliListModel,
    PauliListWrapperModel,
)
from .measure_noise_learning_options_model import MeasureNoiseLearningOptionsModel
from .noise_learner_results_model import (
    NoiseLearnerInputOptionsModel,
    NoiseLearnerResultsMetadataModel,
    NoiseLearnerResultsModel,
)
from .options_model import OptionsModel
from .pec_options_model import PecOptionsModel
from .resilience_options_model import ResilienceOptionsModel
from .twirling_options_model import TwirlingOptionsModel, TwirlingStrategyType
from .zne_options_model import ExtrapolatorType, ZneOptionsModel


class ParamsModel(BaseParamsModel):
    """A model describing the Estimator program inputs."""

    model_config = ConfigDict(extra="forbid")

    schema_version: str = "v0.1"

    pubs: list[EstimatorPubModel]
    """List of Estimator Primitive Unified Blocs (PUBs).

    Each PUB contains a circuit, observables to measure, parameter values, and optional precision.
    """

    support_qiskit: bool = True
    """Whether to support Qiskit-specific features."""

    version: Literal[2] = 2
    """Version number. Must be 2."""

    options: OptionsModel = Field(default_factory=OptionsModel)
    """Options for the Estimator."""

    resilience_level: Annotated[int, Field(ge=0, le=2)] = 1
    """How much resilience to build against errors.
    Higher levels generate more accurate results,
    at the expense of longer processing times.

    * 0: No mitigation.
    * 1: Minimal mitigation costs. Mitigate error associated with readout errors.
    * 2: Medium mitigation costs. Typically reduces bias in estimators but
      is not guaranteed to be zero bias.

    Refer to the
    `Configure error mitigation for Qiskit Runtime
    <https://quantum.cloud.ibm.com/docs/guides/configure-error-mitigation>`_ guide
    for more information about the error mitigation methods used at each level.
    """


__all__ = [
    "DynamicalDecouplingOptionsModel",
    "EstimatorPubModel",
    "ExecutionOptionsV2Model",
    "ExtrapolatorType",
    "NoiseLearnerInputOptionsModel",
    "LayerNoiseLearningOptionsModel",
    "LayerNoiseModel",
    "LayerNoiseWrapperModel",
    "MeasureNoiseLearningOptionsModel",
    "NdarrayWrapperModel",
    "NoiseLearnerResultsModel",
    "OptionsModel",
    "ParamsModel",
    "PauliLindbladErrorModel",
    "PauliLindbladErrorWrapperModel",
    "PauliListModel",
    "PauliListWrapperModel",
    "PecOptionsModel",
    "ResilienceOptionsModel",
    "NoiseLearnerResultsMetadataModel",
    "TwirlingOptionsModel",
    "TwirlingStrategyType",
    "ZneOptionsModel",
]
