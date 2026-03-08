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

"""Validation tests for layer_noise_model_metadata_model.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.models.estimator.version_0_1_dev.output.\
    layer_noise_model_metadata_model import (
        LayerNoiseModelMetadataModel,
        LayerNoiseModelMetadataWrapperModel,
        PauliLindbladErrorMetadataModel,
        PauliLindbladErrorMetadataWrapperModel,
        PauliListMetadataModel,
        PauliListMetadataWrapperModel,
    )
from ibm_quantum_schemas.models.ndarray_wrapper_model import NdarrayWrapperModel
from ibm_quantum_schemas.models.typed_qpy_circuit_model import TypedQpyCircuitModelV13to17


class TestPauliListMetadataModelValidation:
    """Test PauliListMetadataModel validation."""

    def test_valid_pauli_list(self):
        """Test that a valid Pauli list is accepted."""
        data = {"data": ["IXYZ", "ZZII", "XXYY"]}
        model = PauliListMetadataModel.model_validate(data)
        assert model.data == ["IXYZ", "ZZII", "XXYY"]

    def test_valid_empty_pauli_list(self):
        """Test that an empty Pauli list is accepted."""
        data = {"data": []}
        model = PauliListMetadataModel.model_validate(data)
        assert model.data == []

    def test_valid_single_pauli(self):
        """Test that a single Pauli string is accepted."""
        data = {"data": ["X"]}
        model = PauliListMetadataModel.model_validate(data)
        assert model.data == ["X"]

    def test_missing_required_data(self):
        """Test that missing data field is rejected."""
        with pytest.raises(ValidationError, match="Field required"):
            PauliListMetadataModel.model_validate({})

    def test_extra_fields_forbidden(self):
        """Test that extra fields are forbidden."""
        data = {"data": ["X"], "extra_field": "not allowed"}
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            PauliListMetadataModel.model_validate(data)


class TestPauliListMetadataWrapperModelValidation:
    """Test PauliListMetadataWrapperModel validation."""

    def test_valid_wrapper_with_defaults(self):
        """Test that a valid wrapper with default values is accepted."""
        value = PauliListMetadataModel.model_validate({"data": ["X", "Y"]})
        data = {"__value__": value}
        model = PauliListMetadataWrapperModel.model_validate(data)
        assert model.type_ == "settings"
        assert model.module_ == "qiskit.quantum_info.operators.symplectic.pauli_list"
        assert model.class_ == "PauliList"
        assert model.value_.data == ["X", "Y"]

    def test_valid_wrapper_with_explicit_values(self):
        """Test that a valid wrapper with explicit values is accepted."""
        value = PauliListMetadataModel.model_validate({"data": ["Z"]})
        data = {
            "__type__": "settings",
            "__module__": "qiskit.quantum_info.operators.symplectic.pauli_list",
            "__class__": "PauliList",
            "__value__": value,
        }
        model = PauliListMetadataWrapperModel.model_validate(data)
        assert model.type_ == "settings"
        assert model.module_ == "qiskit.quantum_info.operators.symplectic.pauli_list"
        assert model.class_ == "PauliList"

    def test_invalid_type(self):
        """Test that invalid type is rejected."""
        value = PauliListMetadataModel.model_validate({"data": []})
        data = {"__type__": "invalid", "__value__": value}
        with pytest.raises(ValidationError, match="Input should be 'settings'"):
            PauliListMetadataWrapperModel.model_validate(data)

    def test_serialization_uses_aliases(self):
        """Test that serialization uses aliases."""
        value = PauliListMetadataModel.model_validate({"data": ["X"]})
        model = PauliListMetadataWrapperModel.model_validate({"__value__": value})
        serialized = model.model_dump(mode="json")
        assert "__type__" in serialized
        assert "__module__" in serialized
        assert "__class__" in serialized
        assert "__value__" in serialized


class TestPauliLindbladErrorMetadataModelValidation:
    """Test PauliLindbladErrorMetadataModel validation."""

    def test_valid_error_metadata(self, valid_ndarray_wrapper):
        """Test that valid error metadata is accepted."""
        generators = PauliListMetadataWrapperModel.model_validate(
            {"__value__": {"data": ["X", "Y", "Z"]}}
        )
        data = {
            "generators": generators,
            "rates": valid_ndarray_wrapper,
        }
        model = PauliLindbladErrorMetadataModel.model_validate(data)
        assert model.generators == generators
        expected_rates = NdarrayWrapperModel.model_validate(valid_ndarray_wrapper)
        assert model.rates == expected_rates

    def test_missing_required_generators(self, valid_ndarray_wrapper):
        """Test that missing generators is rejected."""
        data = {"rates": valid_ndarray_wrapper}
        with pytest.raises(ValidationError, match="Field required"):
            PauliLindbladErrorMetadataModel.model_validate(data)

    def test_missing_required_rates(self):
        """Test that missing rates is rejected."""
        generators = PauliListMetadataWrapperModel.model_validate({"__value__": {"data": ["X"]}})
        data = {"generators": generators}
        with pytest.raises(ValidationError, match="Field required"):
            PauliLindbladErrorMetadataModel.model_validate(data)

    def test_extra_fields_forbidden(self, valid_ndarray_wrapper):
        """Test that extra fields are forbidden."""
        generators = PauliListMetadataWrapperModel.model_validate({"__value__": {"data": ["X"]}})
        data = {
            "generators": generators,
            "rates": valid_ndarray_wrapper,
            "extra_field": "not allowed",
        }
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            PauliLindbladErrorMetadataModel.model_validate(data)


class TestPauliLindbladErrorMetadataWrapperModelValidation:
    """Test PauliLindbladErrorMetadataWrapperModel validation."""

    def test_valid_wrapper_with_defaults(self, valid_ndarray_wrapper):
        """Test that a valid wrapper with default values is accepted."""
        generators = PauliListMetadataWrapperModel.model_validate({"__value__": {"data": ["X"]}})
        value = PauliLindbladErrorMetadataModel.model_validate(
            {
                "generators": generators,
                "rates": valid_ndarray_wrapper,
            }
        )
        data = {"__value__": value}
        model = PauliLindbladErrorMetadataWrapperModel.model_validate(data)
        assert model.type_ == "_json"
        assert model.module_ == "qiskit_ibm_runtime.utils.noise_learner_result"
        assert model.class_ == "PauliLindbladError"

    def test_serialization_uses_aliases(self, valid_ndarray_wrapper):
        """Test that serialization uses aliases."""
        generators = PauliListMetadataWrapperModel.model_validate({"__value__": {"data": ["X"]}})
        value = PauliLindbladErrorMetadataModel.model_validate(
            {
                "generators": generators,
                "rates": valid_ndarray_wrapper,
            }
        )
        model = PauliLindbladErrorMetadataWrapperModel.model_validate({"__value__": value})
        serialized = model.model_dump(mode="json")
        assert "__type__" in serialized
        assert "__module__" in serialized
        assert "__class__" in serialized
        assert "__value__" in serialized


class TestLayerNoiseModelMetadataModelValidation:
    """Test LayerNoiseModelMetadataModel validation."""

    def test_valid_layer_noise_model(self, valid_typed_qpy_circuit_dict_v13, valid_ndarray_wrapper):
        """Test that valid layer noise model is accepted."""
        generators = PauliListMetadataWrapperModel.model_validate({"__value__": {"data": ["X"]}})
        error = PauliLindbladErrorMetadataWrapperModel.model_validate(
            {
                "__value__": {
                    "generators": generators,
                    "rates": valid_ndarray_wrapper,
                }
            }
        )
        data = {
            "circuit": valid_typed_qpy_circuit_dict_v13,
            "qubits": [0, 1, 2],
            "error": error,
        }
        model = LayerNoiseModelMetadataModel.model_validate(data)
        expected_circuit = TypedQpyCircuitModelV13to17.model_validate(
            valid_typed_qpy_circuit_dict_v13
        )
        assert model.circuit.type_ == expected_circuit.type_
        assert model.circuit.value_ == expected_circuit.value_
        assert model.qubits == [0, 1, 2]
        assert model.error == error

    def test_valid_with_none_error(self, valid_typed_qpy_circuit_dict_v13):
        """Test that layer noise model with None error is accepted."""
        data = {
            "circuit": valid_typed_qpy_circuit_dict_v13,
            "qubits": [0, 1],
            "error": None,
        }
        model = LayerNoiseModelMetadataModel.model_validate(data)
        assert model.error is None

    def test_valid_with_empty_qubits(self, valid_typed_qpy_circuit_dict_v13):
        """Test that layer noise model with empty qubits is accepted."""
        data = {
            "circuit": valid_typed_qpy_circuit_dict_v13,
            "qubits": [],
            "error": None,
        }
        model = LayerNoiseModelMetadataModel.model_validate(data)
        assert model.qubits == []

    def test_missing_required_circuit(self):
        """Test that missing circuit is rejected."""
        data = {"qubits": [0], "error": None}
        with pytest.raises(ValidationError, match="Field required"):
            LayerNoiseModelMetadataModel.model_validate(data)

    def test_missing_required_qubits(self, valid_typed_qpy_circuit_dict_v13):
        """Test that missing qubits is rejected."""
        data = {"circuit": valid_typed_qpy_circuit_dict_v13, "error": None}
        with pytest.raises(ValidationError, match="Field required"):
            LayerNoiseModelMetadataModel.model_validate(data)

    def test_extra_fields_forbidden(self, valid_typed_qpy_circuit_dict_v13):
        """Test that extra fields are forbidden."""
        data = {
            "circuit": valid_typed_qpy_circuit_dict_v13,
            "qubits": [0],
            "error": None,
            "extra_field": "not allowed",
        }
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            LayerNoiseModelMetadataModel.model_validate(data)


class TestLayerNoiseModelMetadataWrapperModelValidation:
    """Test LayerNoiseModelMetadataWrapperModel validation."""

    def test_valid_wrapper_with_defaults(self, valid_typed_qpy_circuit_dict_v13):
        """Test that a valid wrapper with default values is accepted."""
        value = LayerNoiseModelMetadataModel.model_validate(
            {
                "circuit": valid_typed_qpy_circuit_dict_v13,
                "qubits": [0, 1],
                "error": None,
            }
        )
        data = {"__value__": value}
        model = LayerNoiseModelMetadataWrapperModel.model_validate(data)
        assert model.type_ == "_json"
        assert model.module_ == "qiskit_ibm_runtime.utils.noise_learner_result"
        assert model.class_ == "LayerError"

    def test_valid_wrapper_with_explicit_values(self, valid_typed_qpy_circuit_dict_v13):
        """Test that a valid wrapper with explicit values is accepted."""
        value = LayerNoiseModelMetadataModel.model_validate(
            {
                "circuit": valid_typed_qpy_circuit_dict_v13,
                "qubits": [0],
                "error": None,
            }
        )
        data = {
            "__type__": "_json",
            "__module__": "qiskit_ibm_runtime.utils.noise_learner_result",
            "__class__": "LayerError",
            "__value__": value,
        }
        model = LayerNoiseModelMetadataWrapperModel.model_validate(data)
        assert model.type_ == "_json"
        assert model.module_ == "qiskit_ibm_runtime.utils.noise_learner_result"
        assert model.class_ == "LayerError"

    def test_invalid_type(self, valid_typed_qpy_circuit_dict_v13):
        """Test that invalid type is rejected."""
        value = LayerNoiseModelMetadataModel.model_validate(
            {
                "circuit": valid_typed_qpy_circuit_dict_v13,
                "qubits": [],
                "error": None,
            }
        )
        data = {"__type__": "invalid", "__value__": value}
        with pytest.raises(ValidationError, match="Input should be '_json'"):
            LayerNoiseModelMetadataWrapperModel.model_validate(data)

    def test_serialization_uses_aliases(self, valid_typed_qpy_circuit_dict_v13):
        """Test that serialization uses aliases."""
        value = LayerNoiseModelMetadataModel.model_validate(
            {
                "circuit": valid_typed_qpy_circuit_dict_v13,
                "qubits": [0],
                "error": None,
            }
        )
        model = LayerNoiseModelMetadataWrapperModel.model_validate({"__value__": value})
        serialized = model.model_dump(mode="json")
        assert "__type__" in serialized
        assert "__module__" in serialized
        assert "__class__" in serialized
        assert "__value__" in serialized


# Made with Bob
