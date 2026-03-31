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

"""Datetime wrapper model."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class DatetimeWrapperModel(BaseModel):
    """A wrapper around datetime data adding redundant type information."""

    model_config = ConfigDict(populate_by_name=True)

    type_: Literal["datetime"] = Field(default="datetime", alias="__type__")
    """Redundant type information."""

    value_: str = Field(alias="__value__")
    """ISO 8601 formatted datetime string."""
