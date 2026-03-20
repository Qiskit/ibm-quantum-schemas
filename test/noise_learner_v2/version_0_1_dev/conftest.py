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

"""Shared fixtures for noise_learner_v2 validation tests."""

import zlib
from io import BytesIO

import numpy as np
import pybase64
import pytest


@pytest.fixture
def valid_pauli_lindblad_error() -> dict:
    """Fixture to create a valid PauliLindbladError dict."""
    # Create a simple ndarray and encode it
    rates = np.array([0.1, 0.2, 0.3])
    buffer = BytesIO()
    np.save(buffer, rates)
    rates_data = buffer.getvalue()
    compressed = zlib.compress(rates_data)
    encoded = pybase64.b64encode(compressed).decode("utf-8")

    return {
        "__type__": "_json",
        "__module__": "qiskit_ibm_runtime.utils.noise_learner_result",
        "__class__": "PauliLindbladError",
        "__value__": {
            "generators": {
                "__type__": "settings",
                "__module__": "qiskit.quantum_info.operators.symplectic.pauli_list",
                "__class__": "PauliList",
                "__value__": {"data": ["IX", "IY", "IZ"]},
            },
            "rates": {"__type__": "ndarray", "__value__": encoded},
        },
    }


@pytest.fixture
def valid_layer_noise_wrapper(valid_typed_qpy_circuit_dict_v13) -> dict:
    """Fixture to create a valid LayerNoiseWrapperModel dict."""
    return {
        "__type__": "_json",
        "__module__": "qiskit_ibm_runtime.utils.noise_learner_result",
        "__class__": "LayerError",
        "__value__": {
            "circuit": valid_typed_qpy_circuit_dict_v13,
            "qubits": [0, 1],
            "error": None,
        },
    }


@pytest.fixture
def valid_metadata() -> dict:
    """Fixture to create valid metadata dict."""
    return {
        "backend": "ibm_brisbane",
        "input_options": {
            "max_layers_to_learn": 4,
            "shots_per_randomization": 128,
            "num_randomizations": 32,
            "layer_pair_depths": [0, 1, 2],
            "twirling_strategy": "active-accum",
        },
    }
