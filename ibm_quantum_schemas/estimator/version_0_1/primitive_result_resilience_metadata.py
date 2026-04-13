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

"""Primitive result resilience metadata model."""

from __future__ import annotations

from pydantic import BaseModel

from ibm_quantum_schemas.estimator.version_0_1.layer_noise_model_metadata import (
    LayerNoiseModelMetadataWrapperModel,
)
from ibm_quantum_schemas.estimator.version_0_1.primitive_result_zne_metadata import (
    PrimitiveResultZneMetadataModel,
)


class PrimitiveResultResilienceMetadataModel(BaseModel):
    """Primitive result resilience metadata model."""

    measure_mitigation: bool | None = None
    """Whether measure mitigation was applied for the job."""

    zne_mitigation: bool | None = None
    """Whether ZNE mitigation was applied for the job."""

    pec_mitigation: bool | None = None
    """Whether PEC mitigation was applied for the job."""

    zne: PrimitiveResultZneMetadataModel | None = None
    """Metadata about ZNE, applicable if ``zne_mitifation`` is ``True``."""

    layer_noise_model: list[LayerNoiseModelMetadataWrapperModel] | None = None
    """Noise learner results."""
