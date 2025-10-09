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

"""Tests for TensorModel."""

import numpy as np
import pytest

from ibm_quantum_schemas.models.tensor_model import TensorModel


@pytest.mark.parametrize("dtype", [np.uint8, np.float64, np.bool_])
def test_roundtrip(dtype):
    array_in = np.array(range(16), dtype=dtype).reshape(4, 1, 2, 2)
    array_out = TensorModel.from_numpy(array_in).to_numpy()

    assert np.all(array_in == array_out)
