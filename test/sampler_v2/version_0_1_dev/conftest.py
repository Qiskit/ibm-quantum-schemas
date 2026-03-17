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

"""Shared fixtures for sampler validation tests."""

import zlib
from io import BytesIO

import numpy as np
import pybase64
import pytest


@pytest.fixture
def valid_empty_parameter_values() -> dict:
    """Fixture to create empty parameter values as ndarray wrapper."""
    params = np.array([])
    buffer = BytesIO()
    np.save(buffer, params)
    params_data = buffer.getvalue()
    compressed = zlib.compress(params_data)
    encoded = pybase64.b64encode(compressed).decode("utf-8")
    return {"__type__": "ndarray", "__value__": encoded}


@pytest.fixture
def valid_sampler_pub(valid_typed_qpy_circuit_dict_v13, valid_empty_parameter_values) -> list:
    """Fixture to create a valid SamplerPub as a tuple of length 3."""
    return [
        valid_typed_qpy_circuit_dict_v13,
        valid_empty_parameter_values,
        1024,
    ]


@pytest.fixture
def valid_sampler_pub_with_custom_shots(
    valid_typed_qpy_circuit_dict_v13, valid_empty_parameter_values
) -> list:
    """Fixture to create a valid SamplerPub with custom shots."""
    return [
        valid_typed_qpy_circuit_dict_v13,
        valid_empty_parameter_values,
        2048,
    ]
