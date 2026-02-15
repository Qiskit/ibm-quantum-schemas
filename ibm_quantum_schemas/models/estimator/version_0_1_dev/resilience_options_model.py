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

"""Resilience Options Model"""

from __future__ import annotations

from pydantic import BaseModel, Field, model_validator

from ....aliases import Self
from .layer_noise_learning_options_model import LayerNoiseLearningOptionsModel
from .measure_noise_learning_options_model import MeasureNoiseLearningOptionsModel
from .pec_options_model import PecOptionsModel
from .zne_options_model import ZneOptionsModel


class ResilienceOptionsModel(BaseModel):
    """Resilience options for V2 Estimator."""

    measure_mitigation: bool = True
    """Whether to enable measurement error mitigation method.
    
    If you enable measurement mitigation, you can fine-tune its noise learning
    by using :attr:`~measure_noise_learning`. See :class:`MeasureNoiseLearningOptionsModel`
    for all measurement mitigation noise learning options.
    """

    measure_noise_learning: MeasureNoiseLearningOptionsModel = Field(
        default_factory=MeasureNoiseLearningOptionsModel
    )
    """Additional measurement noise learning options.
    
    See :class:`MeasureNoiseLearningOptionsModel` for all options.
    """

    zne_mitigation: bool = False
    """Whether to turn on Zero-Noise Extrapolation error mitigation method.
    
    If you enable ZNE, you can fine-tune its options by using :attr:`~zne`.
    See :class:`ZneOptionsModel` for additional ZNE related options.
    """

    zne: ZneOptionsModel = Field(default_factory=ZneOptionsModel)
    """Additional zero-noise extrapolation mitigation options.
    
    See :class:`ZneOptionsModel` for all options.
    """

    pec_mitigation: bool = False
    """Whether to turn on Probabilistic Error Cancellation error mitigation method.
    
    If you enable PEC, you can fine-tune its options by using :attr:`~pec`.
    See :class:`PecOptionsModel` for additional PEC-related options.
    """

    pec: PecOptionsModel = Field(default_factory=PecOptionsModel)
    """Additional probabilistic error cancellation mitigation options.
    
    See :class:`PecOptionsModel` for all options.
    """

    layer_noise_learning: LayerNoiseLearningOptionsModel = Field(
        default_factory=LayerNoiseLearningOptionsModel
    )
    """Layer noise learning options.
    
    See :class:`LayerNoiseLearningOptionsModel` for all options.
    """

    layer_noise_model: None = None
    """A NoiseLearnerResult or a sequence of LayerError objects.
    
    If ``None``, all the mitigation strategies that require noise data (e.g., PEC
    and PEA) perform a noise-learning stage. Otherwise, this noise-learning stage is skipped,
    and instead gather the required information from ``layer_noise_model``. Layers whose
    information is missing in ``layer_noise_model`` are treated as noiseless and their noise is
    not mitigated.
    """

    @model_validator(mode="after")
    def _validate_options(self) -> Self:
        """Validate the model."""
        # Validate not ZNE+PEC
        if self.pec_mitigation is True and self.zne_mitigation is True:
            raise ValueError(
                "'pec_mitigation' and 'zne_mitigation' options cannot be "
                "simultaneously enabled. Set one of them to False."
            )

        return self

