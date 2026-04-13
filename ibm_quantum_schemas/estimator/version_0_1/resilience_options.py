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

from collections.abc import Sequence

from pydantic import BaseModel, Field, model_validator

from ibm_quantum_schemas.aliases import Self
from ibm_quantum_schemas.estimator.version_0_1.layer_noise_learning_options import (
    LayerNoiseLearningOptionsModel,
)
from ibm_quantum_schemas.estimator.version_0_1.layer_noise_model import (
    LayerNoiseModelWrapperModel,
)
from ibm_quantum_schemas.estimator.version_0_1.measure_noise_learning_options import (
    MeasureNoiseLearningOptionsModel,
)
from ibm_quantum_schemas.estimator.version_0_1.noise_learner_results import (
    NoiseLearnerResultWrapperModel,
)
from ibm_quantum_schemas.estimator.version_0_1.pec_options import PecOptionsModel
from ibm_quantum_schemas.estimator.version_0_1.zne_options import ZneOptionsModel


class ResilienceOptionsModel(BaseModel):
    """Resilience options for V2 Estimator."""

    measure_mitigation: bool | None = None
    """Whether to enable measurement error mitigation method.

    If you enable measurement mitigation, you can fine-tune its noise learning
    by using :attr:`~measure_noise_learning`. See :class:`MeasureNoiseLearningOptionsModel`
    for all measurement mitigation noise learning options.

    If ``measure_mitigation`` is ``None``, it is determined by the server according to the
    resilience level: it is ``False`` for resilience level 0, and ``True`` for resilience
    levels 1 and 2.
    """

    measure_noise_learning: MeasureNoiseLearningOptionsModel = Field(
        default_factory=MeasureNoiseLearningOptionsModel
    )
    """Additional measurement noise learning options.

    See :class:`MeasureNoiseLearningOptionsModel` for all options.
    """

    zne_mitigation: bool | None = None
    """Whether to turn on Zero-Noise Extrapolation error mitigation method.

    If you enable ZNE, you can fine-tune its options by using :attr:`~zne`.
    See :class:`ZneOptionsModel` for additional ZNE related options.

    If ``zne_mitigation`` is ``None``, it is determined by the server according to the
    resilience level: it is ``False`` for resilience levels 0 and 1, and ``True`` for resilience
    level 2.
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

    layer_noise_model: (
        NoiseLearnerResultWrapperModel | Sequence[LayerNoiseModelWrapperModel] | None
    ) = None
    """A noise learner result or a sequence of LayerError objects.

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
