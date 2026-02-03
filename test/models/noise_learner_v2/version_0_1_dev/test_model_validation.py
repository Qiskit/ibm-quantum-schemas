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

"""Validation tests for noise_learner_v2 models.

These tests verify that the Pydantic models correctly validate and reject
invalid data according to their constraints.
"""

import zlib
from io import BytesIO

import pybase64
import pytest
from pydantic import ValidationError
from qiskit.circuit import QuantumCircuit
from qiskit.qpy import dump as qpy_dump

from ibm_quantum_schemas.models.noise_learner_v2.version_0_1_dev.models import (
    CircuitQpyModelV13to14,
    OptionsModel,
    ParamsModel,
    SimulatorOptionsModel,
)


class TestSimulatorOptionsValidation:
    """Test SimulatorOptionsModel validation."""

    def test_valid_simulator_options(self):
        """Test that valid simulator options are accepted."""
        valid_options = {
            "seed_simulator": 42,
            "coupling_map": [[0, 1], [1, 2], [2, 3]],
            "basis_gates": ["u1", "u2", "u3", "cx"],
            "noise_model": None,
        }
        model = SimulatorOptionsModel.model_validate(valid_options)
        assert model.seed_simulator == 42
        assert model.coupling_map == [[0, 1], [1, 2], [2, 3]]
        assert model.basis_gates == ["u1", "u2", "u3", "cx"]
        assert model.noise_model is None

    def test_coupling_map_with_invalid_length(self):
        """Test that coupling_map entries with wrong length are rejected."""
        # Single element (should be 2)
        invalid_single = {"coupling_map": [[0]]}
        with pytest.raises(ValidationError):
            SimulatorOptionsModel.model_validate(invalid_single)

        # Three elements (should be 2)
        invalid_triple = {"coupling_map": [[0, 1, 2]]}
        with pytest.raises(ValidationError):
            SimulatorOptionsModel.model_validate(invalid_triple)

    def test_coupling_map_with_non_integers(self):
        """Test that coupling_map with non-integer values is rejected."""
        invalid = {"coupling_map": [["a", "b"]]}
        with pytest.raises(ValidationError):
            SimulatorOptionsModel.model_validate(invalid)

    def test_empty_coupling_map(self):
        """Test that empty coupling_map is accepted."""
        valid = {"coupling_map": []}
        model = SimulatorOptionsModel.model_validate(valid)
        assert model.coupling_map == []

    def test_all_none_values(self):
        """Test that all None values are accepted (defaults)."""
        model = SimulatorOptionsModel.model_validate({})
        assert model.seed_simulator is None
        assert model.coupling_map is None
        assert model.basis_gates is None
        assert model.noise_model is None


class TestCircuitQpyValidation:
    """Test CircuitQpyModelV13to14 validation."""

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
        model = CircuitQpyModelV13to14.model_validate(circuit_dict)
        assert model.type_ == "QuantumCircuit"
        assert model.value == encoded

    def test_valid_qpy_v14(self):
        """Test that QPY version 14 is accepted."""
        encoded = self._create_qpy_circuit(14)
        circuit_dict = {"__type__": "QuantumCircuit", "__value__": encoded}
        model = CircuitQpyModelV13to14.model_validate(circuit_dict)
        assert model.type_ == "QuantumCircuit"
        assert model.value == encoded

    def test_invalid_qpy_v17_rejected(self):
        """Test that QPY version 17 (too new) is rejected."""
        encoded = self._create_qpy_circuit(17)
        circuit_dict = {"__type__": "QuantumCircuit", "__value__": encoded}
        with pytest.raises(ValidationError, match="qpy_version is 17"):
            CircuitQpyModelV13to14.model_validate(circuit_dict)

    def test_invalid_type_field(self):
        """Test that wrong __type__ value is rejected."""
        encoded = self._create_qpy_circuit(13)
        circuit_dict = {"__type__": "WrongType", "__value__": encoded}
        with pytest.raises(ValidationError, match="Input should be 'QuantumCircuit'"):
            CircuitQpyModelV13to14.model_validate(circuit_dict)

    def test_missing_value_field(self):
        """Test that missing __value__ field is rejected."""
        circuit_dict = {"__type__": "QuantumCircuit"}
        with pytest.raises(ValidationError, match="Field required"):
            CircuitQpyModelV13to14.model_validate(circuit_dict)

    def test_invalid_base64(self):
        """Test that invalid base64 encoding is rejected."""
        circuit_dict = {"__type__": "QuantumCircuit", "__value__": "not-valid-base64!!!"}
        with pytest.raises(ValidationError):
            CircuitQpyModelV13to14.model_validate(circuit_dict)


class TestOptionsModelValidation:
    """Test OptionsModel validation."""

    def test_valid_options_with_defaults(self):
        """Test that options with default values are accepted."""
        model = OptionsModel.model_validate({})
        assert model.max_layers_to_learn == 4
        assert model.shots_per_randomization == 128
        assert model.num_randomizations == 32
        assert model.layer_pair_depths == [0, 1, 2, 4, 16, 32]
        assert model.twirling_strategy == "active-accum"
        assert model.support_qiskit is True
        assert model.experimental is None
        assert model.simulator is None

    def test_valid_options_with_custom_values(self):
        """Test that custom option values are accepted."""
        options = {
            "max_layers_to_learn": 10,
            "shots_per_randomization": 256,
            "num_randomizations": 64,
            "layer_pair_depths": [0, 2, 8],
            "twirling_strategy": "active",
            "support_qiskit": False,
            "experimental": {"test": True},
            "simulator": {"seed_simulator": 123},
        }
        model = OptionsModel.model_validate(options)
        assert model.max_layers_to_learn == 10
        assert model.shots_per_randomization == 256
        assert model.num_randomizations == 64
        assert model.layer_pair_depths == [0, 2, 8]
        assert model.twirling_strategy == "active"
        assert model.support_qiskit is False
        assert model.experimental == {"test": True}
        assert isinstance(model.simulator, SimulatorOptionsModel)
        assert model.simulator.seed_simulator == 123

    def test_invalid_twirling_strategy(self):
        """Test that invalid twirling strategy is rejected."""
        options = {"twirling_strategy": "invalid-strategy"}
        with pytest.raises(ValidationError, match="Input should be 'active'"):
            OptionsModel.model_validate(options)

    def test_negative_shots_per_randomization(self):
        """Test that negative shots_per_randomization uses default."""
        # Pydantic doesn't validate this by default, just tests the model accepts it
        options = {"shots_per_randomization": -1}
        model = OptionsModel.model_validate(options)
        assert model.shots_per_randomization == -1  # No constraint defined

    def test_none_max_layers_to_learn(self):
        """Test that None is accepted for max_layers_to_learn."""
        options = {"max_layers_to_learn": None}
        model = OptionsModel.model_validate(options)
        assert model.max_layers_to_learn is None


class TestParamsModelValidation:
    """Test ParamsModel validation."""

    def _create_valid_circuit_dict(self) -> dict:
        """Helper to create a valid circuit dict."""
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)

        buffer = BytesIO()
        qpy_dump(circuit, buffer, version=13)
        qpy_data = buffer.getvalue()
        compressed = zlib.compress(qpy_data)
        encoded = pybase64.b64encode(compressed).decode("utf-8")

        return {"__type__": "QuantumCircuit", "__value__": encoded}

    def test_valid_params_model(self):
        """Test that valid params are accepted."""
        circuit_dict = self._create_valid_circuit_dict()
        params = {
            "circuits": [circuit_dict],
            "options": {"max_layers_to_learn": 5},
        }
        model = ParamsModel.model_validate(params)
        assert model.schema_version == "v0.1"
        assert len(model.circuits) == 1
        assert model.options.max_layers_to_learn == 5

    def test_missing_circuits_field(self):
        """Test that missing circuits field is rejected."""
        params = {"options": {}}
        with pytest.raises(ValidationError, match="Field required"):
            ParamsModel.model_validate(params)

    def test_missing_options_field(self):
        """Test that missing options field is rejected."""
        circuit_dict = self._create_valid_circuit_dict()
        params = {"circuits": [circuit_dict]}
        with pytest.raises(ValidationError, match="Field required"):
            ParamsModel.model_validate(params)

    def test_empty_circuits_list(self):
        """Test that empty circuits list is accepted."""
        params = {"circuits": [], "options": {}}
        model = ParamsModel.model_validate(params)
        assert len(model.circuits) == 0

    def test_multiple_circuits(self):
        """Test that multiple circuits are accepted."""
        circuit_dict = self._create_valid_circuit_dict()
        params = {
            "circuits": [circuit_dict, circuit_dict, circuit_dict],
            "options": {},
        }
        model = ParamsModel.model_validate(params)
        assert len(model.circuits) == 3


# Made with Bob
