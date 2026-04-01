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

from typing import Annotated, Literal

from pydantic import BaseModel, Field


class LayerNoiseMetadataModel(BaseModel):
    """Metadata about layer noise."""

    noise_overhead: float | Literal["infinity"] | None = None
    """Overall noise overhead."""

    total_mitigated_layers: Annotated[int, Field(ge=0)] | None = None
    """Number of mitigated layers, including duplications of unique layers."""

    unique_mitigated_layers: Annotated[int, Field(ge=0)] | None = None
    """Number of unique mitigated layers."""

    unique_mitigated_layers_noise_overhead: list[float | Literal["infinity"]] | None = None
    """Noise overhead per unique layer."""
