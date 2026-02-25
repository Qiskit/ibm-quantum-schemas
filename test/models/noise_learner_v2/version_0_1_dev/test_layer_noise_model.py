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

from ibm_quantum_schemas.models.noise_learner_v2.version_0_1_dev.layer_noise_model import (
    LayerNoiseModel,
    PauliLindbladErrorWrapperModel,
)


class TestLayerNoiseModelValidation:
    """Test LayerNoiseModel validation."""

    def test_valid_layer_noise_with_error(
        self, valid_typed_qpy_circuit_dict_v13, valid_pauli_lindblad_error
    ):
        """Test that valid LayerNoiseModel with error is accepted."""
        layer_noise = {
            "circuit": valid_typed_qpy_circuit_dict_v13,
            "qubits": [0, 1],
            "error": valid_pauli_lindblad_error,
        }
        model = LayerNoiseModel.model_validate(layer_noise)
        assert model.qubits == [0, 1]
        assert model.error is not None
        assert isinstance(model.error, PauliLindbladErrorWrapperModel)

    def test_optional_error_field_none(self, valid_typed_qpy_circuit_dict_v13):
        """Test that error field can be None (optional)."""
        layer_noise = {
            "circuit": valid_typed_qpy_circuit_dict_v13,
            "qubits": [0, 1],
            "error": None,
        }
        model = LayerNoiseModel.model_validate(layer_noise)
        assert model.qubits == [0, 1]
        assert model.error is None

    def test_optional_error_field_omitted(self, valid_typed_qpy_circuit_dict_v13):
        """Test that error field can be omitted (defaults to None)."""
        layer_noise = {
            "circuit": valid_typed_qpy_circuit_dict_v13,
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

    def test_missing_required_qubits_field(self, valid_typed_qpy_circuit_dict_v13):
        """Test that missing qubits field is rejected."""
        layer_noise = {"circuit": valid_typed_qpy_circuit_dict_v13}
        with pytest.raises(ValidationError, match="Field required"):
            LayerNoiseModel.model_validate(layer_noise)
