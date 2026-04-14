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

"""Params Model"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ibm_quantum_schemas.sampler.version_0_1.options import OptionsModel
from ibm_quantum_schemas.sampler.version_0_1.sampler_pub import SamplerPubModel


class ParamsModel(BaseModel):
    """A model describing the Sampler program inputs."""

    model_config = ConfigDict(extra="forbid")

    pubs: list[SamplerPubModel]
    """List of Sampler Primitive Unified Blocs (PUBs).

    Each PUB contains a circuit, parameter values, and shots.
    """

    support_qiskit: bool = True
    """Whether to support Qiskit-specific features."""

    version: Literal[2] = 2
    """Version number. Must be 2."""

    options: OptionsModel = Field(default_factory=OptionsModel)
    """Options for the Sampler."""
