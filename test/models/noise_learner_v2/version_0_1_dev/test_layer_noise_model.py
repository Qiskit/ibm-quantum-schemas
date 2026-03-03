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


class TestSerializeByAlias:
    """Test that models with aliases serialize correctly."""

    def test_pauli_list_wrapper_serializes_with_aliases(self):
        """Test that PauliListWrapperModel serializes with aliases."""
        from ibm_quantum_schemas.models.noise_learner_v2.version_0_1_dev.layer_noise_model import (
            PauliListWrapperModel,
        )

        # Create using alias names in dict
        wrapper_data = {
            "__type__": "settings",
            "__module__": "qiskit.quantum_info.operators.symplectic.pauli_list",
            "__class__": "PauliList",
            "__value__": {"data": ["XX", "YY"]},
        }
        wrapper = PauliListWrapperModel.model_validate(wrapper_data)

        serialized = wrapper.model_dump(mode="json")
        assert "__type__" in serialized
        assert "__module__" in serialized
        assert "__class__" in serialized
        assert "__value__" in serialized
        assert serialized["__type__"] == "settings"
        assert serialized["__class__"] == "PauliList"

    def test_pauli_lindblad_error_wrapper_serializes_with_aliases(self, valid_pauli_lindblad_error):
        """Test that PauliLindbladErrorWrapperModel serializes with aliases."""
        # valid_pauli_lindblad_error is already a wrapper
        model = PauliLindbladErrorWrapperModel.model_validate(valid_pauli_lindblad_error)

        serialized = model.model_dump(mode="json")
        assert "__type__" in serialized
        assert "__module__" in serialized
        assert "__class__" in serialized
        assert "__value__" in serialized
        assert serialized["__type__"] == "_json"
        assert serialized["__class__"] == "PauliLindbladError"

    def test_layer_noise_wrapper_serializes_with_aliases(
        self, valid_typed_qpy_circuit_dict_v13, valid_pauli_lindblad_error
    ):
        """Test that LayerNoiseWrapperModel serializes with aliases."""
        from ibm_quantum_schemas.models.noise_learner_v2.version_0_1_dev.layer_noise_model import (
            LayerNoiseWrapperModel,
        )

        layer_noise = {
            "circuit": valid_typed_qpy_circuit_dict_v13,
            "qubits": [0, 1],
            "error": valid_pauli_lindblad_error,
        }
        wrapper_data = {
            "__type__": "_json",
            "__module__": "qiskit_ibm_runtime.utils.noise_learner_result",
            "__class__": "LayerError",
            "__value__": layer_noise,
        }
        model = LayerNoiseWrapperModel.model_validate(wrapper_data)

        serialized = model.model_dump(mode="json")
        assert "__type__" in serialized
        assert "__module__" in serialized
        assert "__class__" in serialized
        assert "__value__" in serialized
        assert serialized["__type__"] == "_json"
        assert serialized["__class__"] == "LayerError"

    def test_noise_model_serializes_with_aliases(self):
        """Test that NoiseModel serializes with aliases."""
        from ibm_quantum_schemas.models.noise_learner_v2.version_0_1_dev.options_model import (
            NoiseModel,
        )

        noise_model_data = {"__type__": "NoiseModel", "__value__": {"some": "data"}}
        model = NoiseModel.model_validate(noise_model_data)

        serialized = model.model_dump(mode="json")
        assert "__type__" in serialized
        assert "__value__" in serialized
        assert serialized["__type__"] == "NoiseModel"
