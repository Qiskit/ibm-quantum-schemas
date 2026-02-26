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
"""Typed QPY circuit model stored in zlib compressed form."""

import struct
import zlib
from io import BytesIO
from typing import Literal

import pybase64
from pydantic import BaseModel, Field, model_validator
from qiskit.qpy.formats import FILE_HEADER_V10, FILE_HEADER_V10_PACK, FILE_HEADER_V10_SIZE


def _validate_qpy_version_range(value: str, min_version: int, max_version: int) -> None:
    """Validate that a base64-encoded QPY circuit is within the specified version range.

    Args:
        value: Base64-encoded string containing zlib-compressed QPY serialization.
        min_version: Minimum allowed QPY version (inclusive).
        max_version: Maximum allowed QPY version (inclusive).

    Raises:
        ValueError: If the QPY version is outside the allowed range or if the data
            doesn't contain exactly one quantum circuit.
    """
    # Decode base64 and decompress
    compressed_data = pybase64.b64decode(value)
    qpy_data = zlib.decompress(compressed_data)

    # Read QPY header
    with BytesIO(qpy_data) as bytes_obj:
        header = FILE_HEADER_V10._make(
            struct.unpack(
                FILE_HEADER_V10_PACK,
                bytes_obj.read(FILE_HEADER_V10_SIZE),
            )
        )
        if header.qpy_version < min_version or header.qpy_version > max_version:
            raise ValueError(
                f"The qpy_version is {header.qpy_version} but this model expects the version "
                f"to be between {min_version} and {max_version}."
            )
        if header.num_programs != 1:
            raise ValueError(
                f"Expected exactly one encoded quantum circuit, received {header.num_programs}"
            )


class TypedQpyCircuitModel(BaseModel):
    """A circuit representation used in some primitives.

    This differs from QpyModel in that it contains redundant type information,
    stores the QPY data in zlib compressed form, is only intended to store Circuits
    and does not include the QPY version as a field.
    """

    type_: Literal["QuantumCircuit"] = Field(default="QuantumCircuit", alias="__type__")
    """Redundant type information."""

    value_: str = Field(alias="__value__")
    """
    Base64-encoded string containing zlib-compressed QPY serialization of the quantum circuit.
    """


class TypedQpyCircuitModelV13to17(TypedQpyCircuitModel):
    """A circuit representation with QPY versions constrained to 13-17."""

    @model_validator(mode="after")
    def validate_qpy_version(self):
        """Constrain the allowed QPY version."""
        _validate_qpy_version_range(self.value_, 13, 17)
        return self
