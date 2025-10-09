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
from typing import Literal

import numpy as np
import pybase64
from pydantic import BaseModel, model_validator


class TensorModel(BaseModel):
    """Model of tensor data."""

    _ELEM_SIZE_LOOKUP = {"f64": 8, "u8": 1, "bool": 0.125}

    data: str
    """Base-64-encoded data in litte endian format.

    Bool arrays are bitpacked, other types are IEEE753. Everything is little-endian.
    Tensors are C-ordering.
    """

    shape: list[int]
    """The shape of the tensor."""

    dtype: Literal["f64", "bool", "u8"]
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
        else:
            raise ValueError(
                f"Unexpected NumPy dtype {array.dtype}, one of {cls.dtype.__annotation__} expected."
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
