# This code is a Qiskit project.
#
# (C) Copyright IBM 2025.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""TensorModel"""

import math
import zlib
from typing import Literal, TypeAlias, get_args

import numpy as np
import pybase64
from pydantic import BaseModel, model_validator
from typing_extensions import Buffer

SupportedDtypes: TypeAlias = Literal["f64", "bool", "u8", "c128"]
"""The data types supported by :class:`~TensorModel`."""


def _from_buffer(raw: Buffer, dtype: SupportedDtypes, shape: tuple[int, ...]) -> np.ndarray:
    """Convert a buffer of bytes into a NumPy array of the specified dtype and shape.

    Args:
        raw: The buffer of bytes to convert.
        dtype: The data type of the resulting NumPy array.
        shape: The shape of the resulting NumPy array.

    Returns:
        A NumPy array of the specified dtype and shape.

    Raises:
        ValueError: If the dtype is not supported.
    """
    if dtype == "f64":
        return np.frombuffer(raw, dtype="<f8").reshape(shape)
    elif dtype == "bool":
        # Total number of elements from shape
        total = np.prod(shape, dtype=int)
        unpacked = np.unpackbits(np.frombuffer(raw, dtype=np.uint8), bitorder="little")[:total]
        return unpacked.astype(bool).reshape(shape)
    elif dtype == "u8":
        return np.frombuffer(raw, dtype="<u1").reshape(shape)
    elif dtype == "c128":
        return np.frombuffer(raw, dtype="<c16").reshape(shape)

    raise ValueError(f"dtype {dtype} not understood.")


def _get_dtype_and_bytes(array: np.ndarray) -> tuple[SupportedDtypes, bytes]:
    """Get the dtype string and bytes representation of a NumPy array.

    Args:
        array: The NumPy array to convert.

    Returns:
        A tuple containing the dtype string and the bytes representation of the array.

    Raises:
        ValueError: If the dtype of the array is not supported.
    """
    if array.dtype == np.dtype(np.float64):
        dtype = "f64"
        byte_data = array.astype("<f8").tobytes()
    elif array.dtype == np.dtype(np.bool_):
        dtype = "bool"
        byte_data = np.packbits(array.astype(np.uint8), bitorder="little").tobytes()
    elif array.dtype == np.dtype(np.uint8):
        dtype = "u8"
        byte_data = array.astype("<u1").tobytes()
    elif array.dtype == np.dtype(np.complex128):
        dtype = "c128"
        byte_data = array.astype("<c16").tobytes()
    else:
        raise ValueError(
            f"Unexpected NumPy dtype '{array.dtype}', one of {get_args(SupportedDtypes)} "
            "expected."
        )
    return dtype, byte_data


class TensorModel(BaseModel):
    """Model of tensor data."""

    _ELEM_SIZE_LOOKUP = {"f64": 8, "u8": 1, "bool": 0.125, "c128": 16}

    data: str
    """Base-64-encoded data in litte endian format.

    Bool arrays are bitpacked, other types are IEEE753. Everything is little-endian.
    Tensors are C-ordering.
    """

    shape: list[int]
    """The shape of the tensor."""

    dtype: SupportedDtypes
    """The data type of the tensor."""

    @classmethod
    def from_numpy(cls, array: np.ndarray):
        """Instantiate from a NumPy array."""
        dtype, data = _get_dtype_and_bytes(array)
        encoded_data = pybase64.b64encode(data).decode("utf-8")
        return cls(data=encoded_data, shape=array.shape, dtype=dtype)

    def to_numpy(self) -> np.ndarray:
        """Convert to a NumPy Array."""
        shape = tuple(self.shape)
        raw = pybase64.b64decode(self.data)
        return _from_buffer(raw, self.dtype, shape)

    @model_validator(mode="after")
    def check_sizes(self):
        """Cross-validate that all sizes are consistent."""
        elem_size = self._ELEM_SIZE_LOOKUP[self.dtype]

        # each character encodes 6 bits, each set of 4 characters is therefore 3 bytes
        # finally, suffixed with `=` to force a whole number of bytes.
        len_data = (len(self.data) // 4) * 3 - self.data[-2:].count("=")

        if math.ceil(math.prod(self.shape) * elem_size) != len_data:
            raise ValueError(
                f"Data length {len_data} is inconsistent with shape {self.shape} packed at "
                f"{elem_size} bytes per element."
            )
        return self


class F64TensorModel(TensorModel):
    """Model of tensor data specialized to f64."""

    dtype: Literal["f64"] = "f64"


class CompressableTensorModel(TensorModel):
    """Model of tensor data specialized to compressable types."""

    compressed: bool = True
    """Whether the data has been compressed or not."""

    @classmethod
    def from_numpy(cls, array: np.ndarray, compress: bool = True):
        """Instantiate from a NumPy array."""
        dtype, data = _get_dtype_and_bytes(array)
        if compress:
            data = zlib.compress(data)
        encoded_data = pybase64.b64encode(data).decode("utf-8")
        return cls(data=encoded_data, shape=array.shape, dtype=dtype, compressed=compress)

    def to_numpy(self) -> np.ndarray:
        """Convert to a NumPy Array."""
        shape = tuple(self.shape)
        raw = pybase64.b64decode(self.data)
        if self.compressed:
            raw = zlib.decompress(raw)
        return _from_buffer(raw, self.dtype, shape)

    @model_validator(mode="after")
    def check_sizes(self):
        """Cross-validate that all sizes are consistent."""
        raw = pybase64.b64decode(self.data)
        if self.compressed:
            raw = zlib.decompress(raw)

        elem_size = self._ELEM_SIZE_LOOKUP[self.dtype]
        if math.ceil(len(raw) / elem_size) != math.prod(self.shape):
            raise ValueError(
                f"Data length {len(raw)} is inconsistent with shape {self.shape} packed at "
                f"{elem_size} bytes per element."
            )
        return self


class F64CompressableTensorModel(CompressableTensorModel):
    """Model of compressable tensor data specialized to f64."""

    dtype: Literal["f64"] = "f64"
