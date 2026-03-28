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

"""Pub result resilience metadata model."""

from __future__ import annotations

from pydantic import BaseModel

from ibm_quantum_schemas.estimator.version_0_1.layer_noise_metadata import (
    LayerNoiseMetadataModel,
)
from ibm_quantum_schemas.estimator.version_0_1.pec_metadata import PecMetadataModel
from ibm_quantum_schemas.estimator.version_0_1.pub_result_zne_metadata import (
    PubResultZneMetadataModel,
)


class PubResultResilienceMetadataModel(BaseModel):
    """Pub result resilience metadata model."""

    pec: PecMetadataModel | None = None
    """Metadata about PEC."""

    layer_noise: LayerNoiseMetadataModel | None = None
    """Metadata about layer noise."""

    zne: PubResultZneMetadataModel | None = None
    """Metadata about ZNE."""
