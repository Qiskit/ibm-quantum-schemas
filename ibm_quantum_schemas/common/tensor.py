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

SupportedDtypes: TypeAlias = Literal["f64", "bool", "u8", "c128"]
"""The data types supported by :class:`~TensorModel`."""

SupportedDtypesExtended: TypeAlias = Literal[
    "f16", "f32", "f64", "bool", "i8", "i16", "i32", "i64", "u8", "u16", "u32", "u64", "c64", "c128"
]
"""The data types supported by :class:`~CompressedTensorModel`."""

SUPPORTED_DTYPE_EXTENDED_MAP: dict[np.dtype, SupportedDtypesExtended] = {
    np.dtype(np.bool): "bool",
    np.dtype(np.float16): "f16",
    np.dtype(np.float32): "f32",
    np.dtype(np.float64): "f64",
    np.dtype(np.int8): "i8",
    np.dtype(np.int16): "i16",
    np.dtype(np.int32): "i32",
    np.dtype(np.int64): "i64",
    np.dtype(np.uint8): "u8",
    np.dtype(np.uint16): "u16",
    np.dtype(np.uint32): "u32",
    np.dtype(np.uint64): "u64",
    np.dtype(np.complex64): "c64",
    np.dtype(np.complex128): "c128",
}
"""A map from NumPy dtypes to :type:`~SupportedDtypesExtended`."""


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
        if array.dtype == np.dtype(np.float64):
            dtype = "f64"
            data = pybase64.b64encode(array.astype("<f8").tobytes())
        elif array.dtype == np.dtype(np.bool_):
            dtype = "bool"
            packed = np.packbits(array.astype(np.uint8), bitorder="little")
            data = pybase64.b64encode(packed.tobytes())
        elif array.dtype == np.dtype(np.uint8):
            dtype = "u8"
            data = pybase64.b64encode(array.astype("<u1").tobytes())
        elif array.dtype == np.dtype(np.complex128):
            dtype = "c128"
            data = pybase64.b64encode(array.astype("<c16").tobytes())
        else:
            raise ValueError(
                f"Unexpected NumPy dtype '{array.dtype}', one of {get_args(SupportedDtypes)} "
                "expected."
            )

        return cls(data=data, shape=array.shape, dtype=dtype)

    def to_numpy(self) -> np.ndarray:
        """Convert to a NumPy Array."""
        shape = tuple(self.shape)
        raw = pybase64.b64decode(self.data)

        if self.dtype == "f64":
            return np.frombuffer(raw, dtype="<f8").reshape(shape)
        elif self.dtype == "bool":
            # Total number of elements from shape
            total = np.prod(shape, dtype=int)
            unpacked = np.unpackbits(np.frombuffer(raw, dtype=np.uint8), bitorder="little")[:total]
            return unpacked.astype(bool).reshape(shape)
        elif self.dtype == "u8":
            return np.frombuffer(raw, dtype="<u1").reshape(shape)
        elif self.dtype == "c128":
            return np.frombuffer(raw, dtype="<c16").reshape(shape)

        raise ValueError(f"dtype {self.dtype} not understood.")

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


class CompressedTensorModel(TensorModel):
    """Model of compressed tensor data."""

    _ELEM_SIZE_LOOKUP = {
        "f16": 2,
        "f32": 4,
        "f64": 8,
        "i8": 1,
        "i16": 2,
        "i32": 4,
        "i64": 8,
        "u8": 1,
        "u16": 2,
        "u32": 4,
        "u64": 8,
        "bool": 0.125,
        "c64": 8,
        "c128": 16,
    }
    """A lookup table for the element sizes of :type:`~SupportedDtypesExtended`."""

    dtype: SupportedDtypesExtended
    """The data type of the tensor."""

    @classmethod
    def from_numpy(cls, array: np.ndarray):
        """Instantiate from a NumPy array."""
        array_dtype = array.dtype
        dtype = SUPPORTED_DTYPE_EXTENDED_MAP.get(array_dtype)
        if dtype is None:
            raise ValueError(
                f"Unexpected NumPy dtype '{array_dtype}', one of "
                f"{get_args(SupportedDtypesExtended)}  expected."
            )
        if array_dtype == np.dtype(np.bool_):
            data = np.packbits(array.astype(np.uint8), bitorder="little").tobytes()
        else:
            data = array.astype(f"<{array_dtype.kind}{array_dtype.itemsize}").tobytes()
        encoded_data = pybase64.b64encode(zlib.compress(data)).decode("utf-8")
        return cls(data=encoded_data, shape=array.shape, dtype=dtype)

    def to_numpy(self) -> np.ndarray:
        """Convert to a NumPy Array."""
        shape = tuple(self.shape)
        raw = zlib.decompress(pybase64.b64decode(self.data))
        if (dtype := self.dtype) not in get_args(SupportedDtypesExtended):
            raise ValueError(f"dtype {dtype} not understood.")

        if dtype == "bool":
            # Total number of elements from shape
            total = np.prod(shape, dtype=int)
            unpacked = np.unpackbits(np.frombuffer(raw, dtype=np.uint8), bitorder="little")[:total]
            return unpacked.astype(bool).reshape(shape)

        dkind, dsize = dtype[0], self._ELEM_SIZE_LOOKUP[dtype]
        return np.frombuffer(raw, dtype=f"<{dkind}{dsize}").reshape(shape)

    @model_validator(mode="after")
    def check_sizes(self):
        """Cross-validate that all sizes are consistent."""
        raw = zlib.decompress(pybase64.b64decode(self.data))
        elem_size = self._ELEM_SIZE_LOOKUP[self.dtype]
        len_data = len(raw)

        if math.ceil(math.prod(self.shape) * elem_size) != len_data:
            raise ValueError(
                f"Data length {len_data} is inconsistent with shape {self.shape} packed at "
                f"{elem_size} bytes per element."
            )
        return self


class F64CompressedTensorModel(CompressedTensorModel):
    """Model of compressed tensor data specialized to f64."""

    dtype: Literal["f64"] = "f64"
