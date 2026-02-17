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

import pytest
from pydantic import ValidationError
from qiskit.circuit import QuantumCircuit

from ibm_quantum_schemas.models.noise_learner_v2.version_0_1_dev.layer_noise_model import (
    LayerNoiseModel,
    PauliLindbladErrorWrapperModel,
)
from test.models.utils import valid_typed_qpy_circuit_dict


class TestLayerNoiseModelValidation:
    """Test LayerNoiseModel validation."""

    def test_valid_layer_noise_with_error(self, valid_pauli_lindblad_error):
        """Test that valid LayerNoiseModel with error is accepted."""
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        layer_noise = {
            "circuit": valid_typed_qpy_circuit_dict(circuit),
            "qubits": [0, 1],
            "error": valid_pauli_lindblad_error,
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
