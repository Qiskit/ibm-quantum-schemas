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

"""Validation tests for layer_noise_model.py classes."""

import zlib
from io import BytesIO

import numpy as np
import pybase64
import pytest
from pydantic import ValidationError
from qiskit.circuit import QuantumCircuit

from ibm_quantum_schemas.models.estimator.version_0_1_dev.layer_noise_model import (
    LayerNoiseModel,
    LayerNoiseWrapperModel,
    NdarrayWrapperModel,
    PauliLindbladErrorModel,
    PauliLindbladErrorWrapperModel,
    PauliListModel,
    PauliListWrapperModel,
)
from test.models.utils import valid_typed_qpy_circuit_dict


@pytest.fixture
def valid_pauli_list() -> dict:
    """Fixture to create a valid PauliList dict."""
    return {"data": ["IX", "IY", "IZ"]}


@pytest.fixture
def valid_pauli_list_wrapper() -> dict:
    """Fixture to create a valid PauliListWrapper dict."""
    return {
        "__type__": "settings",
        "__module__": "qiskit.quantum_info.operators.symplectic.pauli_list",
        "__class__": "PauliList",
        "__value__": {"data": ["IX", "IY", "IZ"]},
    }


@pytest.fixture
def valid_ndarray_wrapper() -> dict:
    """Fixture to create a valid NdarrayWrapper dict."""
    rates = np.array([0.1, 0.2, 0.3])
    buffer = BytesIO()
    np.save(buffer, rates)
    rates_data = buffer.getvalue()
    compressed = zlib.compress(rates_data)
    encoded = pybase64.b64encode(compressed).decode("utf-8")
    return {"__type__": "ndarray", "__value__": encoded}


@pytest.fixture
def valid_pauli_lindblad_error(valid_pauli_list_wrapper, valid_ndarray_wrapper) -> dict:
    """Fixture to create a valid PauliLindbladError dict."""
    return {
        "generators": valid_pauli_list_wrapper,
        "rates": valid_ndarray_wrapper,
    }


@pytest.fixture
def valid_pauli_lindblad_error_wrapper(valid_pauli_lindblad_error) -> dict:
    """Fixture to create a valid PauliLindbladErrorWrapper dict."""
    return {
        "__type__": "_json",
        "__module__": "qiskit_ibm_runtime.utils.noise_learner_result",
        "__class__": "PauliLindbladError",
        "__value__": valid_pauli_lindblad_error,
    }


class TestPauliListModelValidation:
    """Test PauliListModel validation."""

    def test_valid_pauli_list(self, valid_pauli_list):
        """Test that valid PauliList is accepted."""
        model = PauliListModel.model_validate(valid_pauli_list)
        assert model.data == ["IX", "IY", "IZ"]

    def test_empty_pauli_list(self):
        """Test that empty PauliList is accepted."""
        model = PauliListModel.model_validate({"data": []})
        assert model.data == []

    def test_missing_data_field(self):
        """Test that missing data field is rejected."""
        with pytest.raises(ValidationError, match="Field required"):
            PauliListModel.model_validate({})


class TestPauliListWrapperModelValidation:
    """Test PauliListWrapperModel validation."""

    def test_valid_pauli_list_wrapper(self, valid_pauli_list_wrapper):
        """Test that valid PauliListWrapper is accepted."""
        model = PauliListWrapperModel.model_validate(valid_pauli_list_wrapper)
        assert model.value_.data == ["IX", "IY", "IZ"]
        assert model.type_ == "settings"
        assert model.module_ == "qiskit.quantum_info.operators.symplectic.pauli_list"
        assert model.class_ == "PauliList"


class TestNdarrayWrapperModelValidation:
    """Test NdarrayWrapperModel validation."""

    def test_valid_ndarray_wrapper(self, valid_ndarray_wrapper):
        """Test that valid NdarrayWrapper is accepted."""
        model = NdarrayWrapperModel.model_validate(valid_ndarray_wrapper)
        assert model.type_ == "ndarray"
        assert isinstance(model.value_, str)

    def test_missing_value_field(self):
        """Test that missing value field is rejected."""
        with pytest.raises(ValidationError, match="Field required"):
            NdarrayWrapperModel.model_validate({"__type__": "ndarray"})


class TestPauliLindbladErrorModelValidation:
    """Test PauliLindbladErrorModel validation."""

    def test_valid_pauli_lindblad_error(self, valid_pauli_lindblad_error):
        """Test that valid PauliLindbladError is accepted."""
        model = PauliLindbladErrorModel.model_validate(valid_pauli_lindblad_error)
        assert isinstance(model.generators, PauliListWrapperModel)
        assert isinstance(model.rates, NdarrayWrapperModel)

    def test_missing_generators_field(self, valid_ndarray_wrapper):
        """Test that missing generators field is rejected."""
        with pytest.raises(ValidationError, match="Field required"):
            PauliLindbladErrorModel.model_validate({"rates": valid_ndarray_wrapper})

    def test_missing_rates_field(self, valid_pauli_list_wrapper):
        """Test that missing rates field is rejected."""
        with pytest.raises(ValidationError, match="Field required"):
            PauliLindbladErrorModel.model_validate({"generators": valid_pauli_list_wrapper})


class TestPauliLindbladErrorWrapperModelValidation:
    """Test PauliLindbladErrorWrapperModel validation."""

    def test_valid_pauli_lindblad_error_wrapper(self, valid_pauli_lindblad_error_wrapper):
        """Test that valid PauliLindbladErrorWrapper is accepted."""
        model = PauliLindbladErrorWrapperModel.model_validate(valid_pauli_lindblad_error_wrapper)
        assert model.type_ == "_json"
        assert model.module_ == "qiskit_ibm_runtime.utils.noise_learner_result"
        assert model.class_ == "PauliLindbladError"
        assert isinstance(model.value_, PauliLindbladErrorModel)


class TestLayerNoiseModelValidation:
    """Test LayerNoiseModel validation."""

    def test_valid_layer_noise_with_error(self, valid_pauli_lindblad_error_wrapper):
        """Test that valid LayerNoiseModel with error is accepted."""
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        layer_noise = {
            "circuit": valid_typed_qpy_circuit_dict(circuit),
            "qubits": [0, 1],
            "error": valid_pauli_lindblad_error_wrapper,
        }
        model = LayerNoiseModel.model_validate(layer_noise)
        assert model.qubits == [0, 1]
        assert model.error is not None
        assert isinstance(model.error, PauliLindbladErrorWrapperModel)

    def test_optional_error_field_none(self):
        """Test that error field can be None (optional)."""
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        layer_noise = {
            "circuit": valid_typed_qpy_circuit_dict(circuit),
            "qubits": [0, 1],
            "error": None,
        }
        model = LayerNoiseModel.model_validate(layer_noise)
        assert model.qubits == [0, 1]
        assert model.error is None

    def test_optional_error_field_omitted(self):
        """Test that error field can be omitted (defaults to None)."""
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        layer_noise = {
            "circuit": valid_typed_qpy_circuit_dict(circuit),
            "qubits": [0, 1],
        }
        model = LayerNoiseModel.model_validate(layer_noise)
        assert model.qubits == [0, 1]
        assert model.error is None

    def test_missing_required_circuit_field(self):
        """Test that missing circuit field is rejected."""
        layer_noise = {"qubits": [0, 1]}
        with pytest.raises(ValidationError, match="Field required"):
            LayerNoiseModel.model_validate(layer_noise)

    def test_missing_required_qubits_field(self):
        """Test that missing qubits field is rejected."""
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        layer_noise = {"circuit": valid_typed_qpy_circuit_dict(circuit)}
        with pytest.raises(ValidationError, match="Field required"):
            LayerNoiseModel.model_validate(layer_noise)

    def test_empty_qubits_list(self):
        """Test that empty qubits list is accepted."""
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        layer_noise = {
            "circuit": valid_typed_qpy_circuit_dict(circuit),
            "qubits": [],
        }
        model = LayerNoiseModel.model_validate(layer_noise)
        assert model.qubits == []


class TestLayerNoiseWrapperModelValidation:
    """Test LayerNoiseWrapperModel validation."""

    def test_valid_layer_noise_wrapper(self):
        """Test that valid LayerNoiseWrapper is accepted."""
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        wrapper = {
            "__type__": "_json",
            "__module__": "qiskit_ibm_runtime.utils.noise_learner_result",
            "__class__": "LayerError",
            "__value__": {
                "circuit": valid_typed_qpy_circuit_dict(circuit),
                "qubits": [0, 1],
                "error": None,
            },
        }
        model = LayerNoiseWrapperModel.model_validate(wrapper)
        assert model.type_ == "_json"
        assert model.module_ == "qiskit_ibm_runtime.utils.noise_learner_result"
        assert model.class_ == "LayerError"
        assert isinstance(model.value_, LayerNoiseModel)
        assert model.value_.qubits == [0, 1]

# Made with Bob
