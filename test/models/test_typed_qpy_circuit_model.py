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

"""Validation tests for typed_qpy_circuit_model.py classes."""

import zlib
from io import BytesIO

import pybase64
import pytest
from pydantic import ValidationError
from qiskit.circuit import QuantumCircuit
from qiskit.qpy import dump as qpy_dump

from ibm_quantum_schemas.models import typed_qpy_circuit_model as qpy_model


class TestTypedQpyCircuitModelValidation:
    """Test TypedQpyCircuitModelV13to17 validation."""

    def _create_qpy_circuit(self, qpy_version: int) -> str:
        """Helper to create a QPY-encoded circuit with specific version."""
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)

        # Encode to QPY
        buffer = BytesIO()
        qpy_dump(circuit, buffer, version=qpy_version)
        qpy_data = buffer.getvalue()

        # Compress and base64 encode
        compressed = zlib.compress(qpy_data)
        encoded = pybase64.b64encode(compressed).decode("utf-8")
        return encoded

    def test_valid_qpy_v13(self):
        """Test that QPY version 13 is accepted."""
        encoded = self._create_qpy_circuit(13)
        circuit_dict = {"__type__": "QuantumCircuit", "__value__": encoded}
        model = qpy_model.TypedQpyCircuitModelV13to17.model_validate(circuit_dict)
        assert model.type_ == "QuantumCircuit"
        assert model.value_ == encoded

    def test_valid_qpy_v14(self):
        """Test that QPY version 14 is accepted."""
        encoded = self._create_qpy_circuit(14)
        circuit_dict = {"__type__": "QuantumCircuit", "__value__": encoded}
        model = qpy_model.TypedQpyCircuitModelV13to17.model_validate(circuit_dict)
        assert model.type_ == "QuantumCircuit"
        assert model.value_ == encoded

    def test_valid_qpy_v17(self):
        """Test that QPY version 17 is accepted."""
        encoded = self._create_qpy_circuit(17)
        circuit_dict = {"__type__": "QuantumCircuit", "__value__": encoded}
        model = qpy_model.TypedQpyCircuitModelV13to17.model_validate(circuit_dict)
        assert model.type_ == "QuantumCircuit"
        assert model.value_ == encoded

    def test_invalid_type_field(self):
        """Test that wrong __type__ value is rejected."""
        encoded = self._create_qpy_circuit(13)
        circuit_dict = {"__type__": "WrongType", "__value__": encoded}
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
