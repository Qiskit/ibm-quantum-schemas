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

"""Bit Array Model."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ibm_quantum_schemas.common.ndarray_wrapper import NdarrayWrapperModel


class BitArrayModel(BaseModel):
    """Bit array model class.

    A ``BitArray`` represents measurement outcomes as a packed binary array.
    The underlying data is stored as an ``ndarray`` of ``uint8`` values.
    """

    num_bits: int
    """Number of bits per measurement outcome."""

    array: NdarrayWrapperModel
    """The packed binary array data."""


class BitArrayWrapperModel(BaseModel):
    """Bit array wrapper model class."""

    model_config = ConfigDict(serialize_by_alias=True)

    type_: Literal["BitArray"] = Field(default="BitArray", alias="__type__")
    """Redundant type information."""

    value_: BitArrayModel = Field(alias="__value__")
    """The actual data."""
