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

"""Tests for tensor models."""

import numpy as np
import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.models.tensor_model import F64TensorModel, TensorModel


class TestTensorModel:
    """Tests for ``TensorModel``."""

    @pytest.mark.parametrize("dtype", [np.uint8, np.float64, np.bool_])
    def test_roundtrip(self, dtype):
        """Test that round trips work correctly."""
        array = np.array(range(16), dtype=dtype).reshape(4, 1, 2, 2)
        array_out = TensorModel.from_numpy(array).to_numpy()

        assert np.all(array == array_out)

    def test_raises(self):
        """Test that it raises."""
        array = np.array(range(16), dtype=int)

        with pytest.raises(ValueError, match="Unexpected NumPy dtype 'int64'"):
            TensorModel.from_numpy(array)


class TestF64TensorModel:
    """Tests for ``F64TensorModel``."""

    def test_roundtrip(self):
        """Test that round trips work correctly."""
        array = np.array(range(16), dtype=np.float64).reshape(4, 1, 2, 2)
        array_out = F64TensorModel.from_numpy(array).to_numpy()

        assert np.all(array == array_out)

    @pytest.mark.parametrize("dtype", [np.uint8, np.bool_])
    def test_raises(self, dtype):
        """Test that it raises."""
        array = np.array(range(16), dtype=dtype)

        with pytest.raises(ValidationError):
            F64TensorModel.from_numpy(array)
