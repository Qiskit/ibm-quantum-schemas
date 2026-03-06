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

"""Pub Result Model."""


from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field
from typing import Literal, Any

from .data_bin_model import DataBinWrapperModel


class PubResultMetadataModel(BaseModel):
    """Metadata for the estimator v2 job."""

    model_config = ConfigDict(extra="forbid")

    circuit_metadata: dict | None = None
    """Circuit metadata, attached by the user to the input circuit."""

    target_precision: float | None = None
    shots: int | None = None
    num_randomizations: int | None = None

    experimental: dict[str, Any] | None = None
    """Experimental metadata."""


class PubResultModel(BaseModel):
    """A model describing the Estimator program output for a single pub."""

    model_config = ConfigDict(extra="forbid")

    data: DataBinWrapperModel
    """Result data from the estimator v2 job."""

    metadata: PubResultMetadataModel
    """Metadata for the estimator v2 job."""


class PubResultWrapperModel(BaseModel):
    """Pub result wrapper model class.
    """
    
    model_config = ConfigDict(serialize_by_alias=True, extra="forbid")

    type_: Literal["PubResult"] = Field(default="PubResult", alias="__type__")
    """Redundant type information."""

    value_: PubResultModel = Field(alias="__value__")
