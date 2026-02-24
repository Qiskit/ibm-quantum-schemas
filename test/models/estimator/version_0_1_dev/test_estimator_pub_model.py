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

"""Validation tests for estimator_pub_model.py classes."""

import pytest
from pydantic import ValidationError
from qiskit.circuit import QuantumCircuit

from ibm_quantum_schemas.models.estimator.version_0_1_dev.estimator_pub_model import (
    EstimatorPubModel,
)
from test.models.utils import valid_typed_qpy_circuit_dict


class TestEstimatorPubModelValidation:
    """Test EstimatorPubModel validation."""

    def test_valid_estimator_pub_full(
        self, valid_observable, valid_parameter_values, valid_parameterized_circuit
    ):
        """Test that valid EstimatorPub with all fields is accepted (with parameters)."""
        pub = [
            valid_typed_qpy_circuit_dict(valid_parameterized_circuit),
            valid_observable,
            valid_parameter_values,
            0.01,
        ]
        model = EstimatorPubModel.model_validate(pub)
        assert len(model.root) == 4
        
        # Verify circuit element (index 0) - TypedQpyCircuitModelV13to17
        assert model.root[0].type_ == pub[0]["__type__"]
        assert model.root[0].value_ == pub[0]["__value__"]
        
        # Verify observables element (index 1) - ObservablesArrayModel
        assert model.root[1].root == pub[1]
        
        # Verify parameter_values element (index 2) - NdarrayWrapperModel
        assert model.root[2].type_ == pub[2]["__type__"]
        assert model.root[2].value_ == pub[2]["__value__"]
        
        # Verify precision element (index 3)
        assert model.root[3] == pub[3]

    def test_valid_estimator_pub_full_no_parameters(
        self, valid_observable, valid_empty_parameter_values
    ):
        """Test that valid EstimatorPub with all fields is accepted (without parameters)."""
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        pub = [
            valid_typed_qpy_circuit_dict(circuit),
            valid_observable,
            valid_empty_parameter_values,
            0.01,
        ]
        model = EstimatorPubModel.model_validate(pub)
        assert len(model.root) == 4
        
        # Verify circuit element (index 0) - TypedQpyCircuitModelV13to17
        assert model.root[0].type_ == pub[0]["__type__"]
        assert model.root[0].value_ == pub[0]["__value__"]
        
        # Verify observables element (index 1) - ObservablesArrayModel
        assert model.root[1].root == pub[1]
        
        # Verify parameter_values element (index 2) - NdarrayWrapperModel (empty)
        assert model.root[2].type_ == pub[2]["__type__"]
        assert model.root[2].value_ == pub[2]["__value__"]
        
        # Verify precision element (index 3)
        assert model.root[3] == pub[3]

    def test_valid_estimator_pub_without_precision(
        self, valid_observable, valid_parameter_values, valid_parameterized_circuit
    ):
        """Test that EstimatorPub without precision is accepted (defaults to None)."""
        pub = [
            valid_typed_qpy_circuit_dict(valid_parameterized_circuit),
            valid_observable,
            valid_parameter_values,
        ]
        model = EstimatorPubModel.model_validate(pub)
        assert len(model.root) == 4
        
        # Verify circuit element (index 0) - TypedQpyCircuitModelV13to17
        assert model.root[0].type_ == pub[0]["__type__"]
        assert model.root[0].value_ == pub[0]["__value__"]
        
        # Verify observables element (index 1) - ObservablesArrayModel
        assert model.root[1].root == pub[1]
        
        # Verify parameter_values element (index 2) - NdarrayWrapperModel
        assert model.root[2].type_ == pub[2]["__type__"]
        assert model.root[2].value_ == pub[2]["__value__"]
        
        # Verify precision element (index 3) - should be None (default added by model)
        assert model.root[3] is None

    def test_valid_estimator_pub_minimal(self, valid_observable):
        """Test that EstimatorPub with only circuit and observables is accepted."""
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        pub = [
            valid_typed_qpy_circuit_dict(circuit),
            valid_observable,
        ]
        model = EstimatorPubModel.model_validate(pub)
        assert len(model.root) == 4
        
        # Verify circuit element (index 0) - TypedQpyCircuitModelV13to17
        assert model.root[0].type_ == pub[0]["__type__"]
        assert model.root[0].value_ == pub[0]["__value__"]
        
        # Verify observables element (index 1) - ObservablesArrayModel
        assert model.root[1].root == pub[1]
        
        # Verify parameter_values element (index 2) - NdarrayWrapperModel (default empty added by model)
        assert model.root[2].type_ == "ndarray"
        assert isinstance(model.root[2].value_, str)
        
        # Verify precision element (index 3) - should be None (default added by model)
        assert model.root[3] is None

    def test_valid_estimator_pub_with_observables_list(
        self, valid_observables_list, valid_empty_parameter_values
    ):
        """Test that EstimatorPub with list of observables is accepted."""
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        pub = [
            valid_typed_qpy_circuit_dict(circuit),
            valid_observables_list,
            valid_empty_parameter_values,
            None,
        ]
        model = EstimatorPubModel.model_validate(pub)
        assert len(model.root) == 4
        
        # Verify circuit element (index 0) - TypedQpyCircuitModelV13to17
        assert model.root[0].type_ == pub[0]["__type__"]
        assert model.root[0].value_ == pub[0]["__value__"]
        
        # Verify observables element (index 1) - ObservablesArrayModel (list)
        assert model.root[1].root == pub[1]
        
        # Verify parameter_values element (index 2) - NdarrayWrapperModel
        assert model.root[2].type_ == pub[2]["__type__"]
        assert model.root[2].value_ == pub[2]["__value__"]
        
        # Verify precision element (index 3)
        assert model.root[3] is None

    def test_precision_must_be_positive(
        self, valid_observable, valid_empty_parameter_values
    ):
        """Test that precision must be positive."""
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        pub = [
            valid_typed_qpy_circuit_dict(circuit),
            valid_observable,
            valid_empty_parameter_values,
            0.0,
        ]
        with pytest.raises(ValidationError, match="greater than 0"):
            EstimatorPubModel.model_validate(pub)

    def test_negative_precision(
        self, valid_observable, valid_empty_parameter_values
    ):
        """Test that negative precision is rejected."""
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        pub = [
            valid_typed_qpy_circuit_dict(circuit),
            valid_observable,
            valid_empty_parameter_values,
            -0.01,
        ]
        with pytest.raises(ValidationError, match="greater than 0"):
            EstimatorPubModel.model_validate(pub)

    def test_precision_none_is_valid(
        self, valid_observable, valid_empty_parameter_values
    ):
        """Test that precision can be None."""
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        pub = [
            valid_typed_qpy_circuit_dict(circuit),
            valid_observable,
            valid_empty_parameter_values,
            None,
        ]
        model = EstimatorPubModel.model_validate(pub)
        assert len(model.root) == 4
        
        # Verify circuit element (index 0) - TypedQpyCircuitModelV13to17
        assert model.root[0].type_ == pub[0]["__type__"]
        assert model.root[0].value_ == pub[0]["__value__"]
        
        # Verify observables element (index 1) - ObservablesArrayModel
        assert model.root[1].root == pub[1]
        
        # Verify parameter_values element (index 2) - NdarrayWrapperModel
        assert model.root[2].type_ == pub[2]["__type__"]
        
        # Verify precision element (index 3) is None
        assert model.root[3] is None

    def test_too_few_elements(self):
        """Test that tuple with only 1 element is rejected."""
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        pub = [valid_typed_qpy_circuit_dict(circuit)]
        with pytest.raises(ValidationError):
            EstimatorPubModel.model_validate(pub)

    def test_too_many_elements(
        self, valid_observable, valid_empty_parameter_values
    ):
        """Test that tuple with more than 4 elements is rejected."""
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        pub = [
            valid_typed_qpy_circuit_dict(circuit),
            valid_observable,
            valid_empty_parameter_values,
            0.01,
            "extra",
        ]
        with pytest.raises(ValidationError):
            EstimatorPubModel.model_validate(pub)

    def test_invalid_circuit_type(self, valid_observable):
        """Test that invalid circuit type is rejected."""
        pub = [
            "not a circuit",
            valid_observable,
        ]
        with pytest.raises(ValidationError):
            EstimatorPubModel.model_validate(pub)

    def test_invalid_observable_type(self, valid_empty_parameter_values):
        """Test that invalid observable type is rejected."""
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        pub = [
            valid_typed_qpy_circuit_dict(circuit),
            "not an observable",
            valid_empty_parameter_values,
            None,
        ]
        with pytest.raises(ValidationError):
            EstimatorPubModel.model_validate(pub)
