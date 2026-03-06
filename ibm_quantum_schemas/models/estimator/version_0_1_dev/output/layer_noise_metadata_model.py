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

"""Layer Noise Metadata Model."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict


class LayerNoiseMetadataModel(BaseModel):
    """Metadata about layer noise."""

    model_config = ConfigDict(extra="forbid")

    noise_overhead: float | Literal["infinity"] | None = None
    total_mitigated_layers: int | None = None
    unique_mitigated_layers: int | None = None
    unique_mitigated_layers_noise_overhead: list[float | Literal["infinity"]] | None = None

# Made with Bob
