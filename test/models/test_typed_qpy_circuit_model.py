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

"""Validation tests for typed_qpy_circuit_model.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.models import typed_qpy_circuit_model as qpy_model


class TestTypedQpyCircuitModelValidation:
    """Test TypedQpyCircuitModelV13to17 validation."""

    def test_valid_typed_qpy_circuit(self, valid_typed_qpy_circuit_dict_v13):
        """Test that valid TypedQpyCircuitModel is accepted."""
        model = qpy_model.TypedQpyCircuitModelV13to17.model_validate(
            valid_typed_qpy_circuit_dict_v13
        )
        assert model.type_ == "QuantumCircuit"
        assert model.value_ == valid_typed_qpy_circuit_dict_v13["__value__"]

    def test_invalid_type_field(self, compressed_qpy_circuit_v13):
        """Test that wrong __type__ value is rejected."""
        circuit_dict = {"__type__": "WrongType", "__value__": compressed_qpy_circuit_v13}
        with pytest.raises(ValidationError, match="Input should be 'QuantumCircuit'"):
            qpy_model.TypedQpyCircuitModelV13to17.model_validate(circuit_dict)

    def test_missing_value_field(self):
        """Test that missing __value__ field is rejected."""
        circuit_dict = {"__type__": "QuantumCircuit"}
        with pytest.raises(ValidationError, match="Field required"):
            qpy_model.TypedQpyCircuitModelV13to17.model_validate(circuit_dict)

    def test_invalid_base64(self):
        """Test that invalid base64 encoding is rejected."""
        circuit_dict = {"__type__": "QuantumCircuit", "__value__": "not-valid-base64!!!"}
        with pytest.raises(ValidationError):
            qpy_model.TypedQpyCircuitModelV13to17.model_validate(circuit_dict)


class TestTypedQpyCircuitModelV13Validation:
    """Test TypedQpyCircuitModelV13 validation."""

    def test_valid_v13_circuit(self, compressed_qpy_circuit_v13):
        """Test that valid QPY v13 circuit is accepted."""
        circuit_dict = {"__type__": "QuantumCircuit", "__value__": compressed_qpy_circuit_v13}
        model = qpy_model.TypedQpyCircuitModelV13.model_validate(circuit_dict)
        assert model.type_ == "QuantumCircuit"
        assert model.value_ == compressed_qpy_circuit_v13

    def test_invalid_v14_circuit(self, compressed_qpy_circuit_v14):
        """Test that QPY v14 circuit is rejected by V13-only model."""
        circuit_dict = {"__type__": "QuantumCircuit", "__value__": compressed_qpy_circuit_v14}
        with pytest.raises(
            ValidationError,
            match=r"qpy_version is 14 but this model expects the version to be between 13 and 13",
        ):
            qpy_model.TypedQpyCircuitModelV13.model_validate(circuit_dict)
