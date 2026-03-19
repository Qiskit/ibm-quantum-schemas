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

"""Ndarray wrapper model."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class NdarrayWrapperModel(BaseModel):
    """A wrapper around ndarray data adding redundant type information."""

    model_config = ConfigDict(serialize_by_alias=True)

    type_: Literal["ndarray"] = Field(default="ndarray", alias="__type__")
    """Redundant type information."""

    value_: str = Field(alias="__value__")
    """The actual data: Base64-encoded, zlib compressed numpy binary format of an ndarray."""
