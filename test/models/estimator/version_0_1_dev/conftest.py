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

"""Shared fixtures for estimator validation tests."""

import zlib
from io import BytesIO

import numpy as np
import pybase64
import pytest
from qiskit.circuit import Parameter, QuantumCircuit

from test.models.utils import valid_typed_qpy_circuit_dict


@pytest.fixture
def valid_observable() -> dict:
    """Fixture to create a valid observable dict."""
    return {"XX": 0.5, "YY": 0.5}


@pytest.fixture
def valid_observables_list() -> list:
    """Fixture to create a valid list of observables."""
    return [{"XX": 1.0}, {"YY": 1.0, "ZZ": 1.0}]


@pytest.fixture
def valid_parameter_values() -> dict:
    """Fixture to create valid parameter values as ndarray wrapper."""
    params = np.array([0.1, 0.2, 0.3])
    buffer = BytesIO()
    np.save(buffer, params)
    params_data = buffer.getvalue()
    compressed = zlib.compress(params_data)
    encoded = pybase64.b64encode(compressed).decode("utf-8")
    return {"__type__": "ndarray", "__value__": encoded}


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
def valid_estimator_pub(valid_observable, valid_empty_parameter_values) -> list:
    """Fixture to create a valid EstimatorPub as a list."""
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    return [
        valid_typed_qpy_circuit_dict(circuit),
        valid_observable,
        valid_empty_parameter_values,
        None,
    ]


@pytest.fixture
def valid_estimator_pub_with_precision(valid_observable, valid_empty_parameter_values) -> list:
    """Fixture to create a valid EstimatorPub with precision."""
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    return [
        valid_typed_qpy_circuit_dict(circuit),
        valid_observable,
        valid_empty_parameter_values,
        0.01,
    ]


@pytest.fixture
def valid_layer_noise_wrapper() -> dict:
    """Fixture to create a valid LayerNoiseWrapperModel dict."""
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    return {
        "__type__": "_json",
        "__module__": "qiskit_ibm_runtime.utils.noise_learner_result",
        "__class__": "LayerError",
        "__value__": {
            "circuit": valid_typed_qpy_circuit_dict(circuit),
            "qubits": [0, 1],
            "error": None,
        },
    }


@pytest.fixture
def valid_parameterized_circuit() -> QuantumCircuit:
    """Fixture to create a parameterized circuit with 3 parameters."""
    circuit = QuantumCircuit(2)
    theta = Parameter("theta")
    phi = Parameter("phi")
    gamma = Parameter("gamma")
    circuit.ry(theta, 0)
    circuit.rx(phi, 1)
    circuit.rz(gamma, 0)
    circuit.cx(0, 1)
    return circuit
