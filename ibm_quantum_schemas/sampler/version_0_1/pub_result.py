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

"""Pub Result Model for Sampler V2."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ibm_quantum_schemas.sampler.version_0_1.data_bin import DataBinWrapperModel


class PubResultMetadataModel(BaseModel):
    """Metadata for a single pub result in Sampler V2."""

    model_config = ConfigDict(extra="allow")

    circuit_metadata: dict | None = None
    """Circuit metadata, attached by the user to the input circuit."""

    num_randomizations: int | None = None
    """Number of randomizations used for twirling, if twirling was enabled."""


class PubResultModel(BaseModel):
    """A model describing the Sampler V2 program output for a single pub."""

    data: DataBinWrapperModel
    """Result data from the sampler v2 job."""

    metadata: PubResultMetadataModel
    """Metadata for the sampler v2 job."""


class SamplerPubResultWrapperModel(BaseModel):
    """Sampler pub result wrapper model class."""

    model_config = ConfigDict(serialize_by_alias=True)

    type_: Literal["SamplerPubResult"] = Field(default="SamplerPubResult", alias="__type__")
    """Redundant type information."""

    value_: PubResultModel = Field(alias="__value__")
    """The actual data."""
