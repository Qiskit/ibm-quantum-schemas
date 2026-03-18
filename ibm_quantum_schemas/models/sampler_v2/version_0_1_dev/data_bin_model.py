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

"""Data bin models for Sampler V2."""

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class DataBinModel(BaseModel):
    """Data bin model class for Sampler V2."""

    field_names: list[str]
    """Names of fields contained in the data bin."""

    field_types: list[str]
    """Types of fields contained in the data bin."""

    shape: tuple[int, ...]
    """Data bin shape."""

    fields: dict[str, Any]
    """Data bin fields. Typically coontains BitArrayWrapperModel instances for
    classical registers, but could include other metadata."""


class DataBinWrapperModel(BaseModel):
    """Data bin wrapper model class."""

    model_config = ConfigDict(serialize_by_alias=True)

    type_: Literal["DataBin"] = Field(default="DataBin", alias="__type__")
    """Redundant type information."""

    value_: DataBinModel = Field(alias="__value__")
    """The actual data."""
