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

from ibm_quantum_schemas.models import typed_qpy_circuit_model as qpy_model
from ibm_quantum_schemas.models.noise_learner_v2.version_0_1_dev.layer_noise_model import (
    LayerNoiseModel,
    LayerNoiseWrapperModel,
    PauliLindbladErrorWrapperModel,
)
from ibm_quantum_schemas.models.noise_learner_v2.version_0_1_dev.models import (
    OptionsModel,
    ParamsModel,
    ResultsModel,
)
from ibm_quantum_schemas.models.noise_learner_v2.version_0_1_dev.options_model import (
    SimulatorOptionsModel,
)
from ibm_quantum_schemas.models.noise_learner_v2.version_0_1_dev.results_metadata_model import (
    InputOptionsModel,
    ResultsMetadataModel,
)

# Fixtures


@pytest.fixture
def valid_circuit_dict() -> dict:
    """Fixture to create a valid circuit dict."""
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)

    buffer = BytesIO()
    qpy_dump(circuit, buffer, version=13)
    qpy_data = buffer.getvalue()
    compressed = zlib.compress(qpy_data)
    encoded = pybase64.b64encode(compressed).decode("utf-8")

    return {"__type__": "QuantumCircuit", "__value__": encoded}


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

    def test_valid_params_model(self, valid_circuit_dict):
        """Test that valid params are accepted."""
        circuit_dict = valid_circuit_dict
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

    def test_missing_options_field(self, valid_circuit_dict):
        """Test that missing options field is rejected."""
        params = {"circuits": [valid_circuit_dict]}
        with pytest.raises(ValidationError, match="Field required"):
            ParamsModel.model_validate(params)

    def test_empty_circuits_list(self):
        """Test that empty circuits list is accepted."""
        params = {"circuits": [], "options": {}}
        model = ParamsModel.model_validate(params)
        assert len(model.circuits) == 0

    def test_multiple_circuits(self, valid_circuit_dict):
        """Test that multiple circuits are accepted."""
        circuit_dict = valid_circuit_dict
        params = {
            "circuits": [circuit_dict, circuit_dict, circuit_dict],
            "options": {},
        }
        model = ParamsModel.model_validate(params)
        assert len(model.circuits) == 3


class TestInputOptionsModelValidation:
    """Test InputOptionsModel validation."""

    def test_valid_input_options(self):
        """Test that valid input options are accepted."""
        options = {
            "max_layers_to_learn": 4,
            "shots_per_randomization": 128,
            "num_randomizations": 32,
            "layer_pair_depths": [0, 1, 2, 4, 16, 32],
            "twirling_strategy": "active-accum",
        }
        model = InputOptionsModel.model_validate(options)
        assert model.max_layers_to_learn == 4
        assert model.shots_per_randomization == 128
        assert model.num_randomizations == 32
        assert model.layer_pair_depths == [0, 1, 2, 4, 16, 32]
        assert model.twirling_strategy == "active-accum"

    def test_optional_max_layers_to_learn(self):
        """Test that max_layers_to_learn can be None."""
        options = {
            "max_layers_to_learn": None,
            "shots_per_randomization": 128,
            "num_randomizations": 32,
            "layer_pair_depths": [0, 1],
            "twirling_strategy": "active",
        }
        model = InputOptionsModel.model_validate(options)
        assert model.max_layers_to_learn is None

    def test_invalid_twirling_strategy_in_input_options(self):
        """Test that invalid twirling strategy is rejected."""
        options = {
            "max_layers_to_learn": 4,
            "shots_per_randomization": 128,
            "num_randomizations": 32,
            "layer_pair_depths": [0, 1],
            "twirling_strategy": "invalid",
        }
        with pytest.raises(ValidationError, match="Input should be 'active'"):
            InputOptionsModel.model_validate(options)


class TestResultsMetadataModelValidation:
    """Test ResultsMetadataModel validation."""

    def test_valid_results_metadata(self):
        """Test that valid results metadata is accepted."""
        metadata = {
            "backend": "some_backend",
            "input_options": {
                "max_layers_to_learn": 4,
                "shots_per_randomization": 128,
                "num_randomizations": 32,
                "layer_pair_depths": [0, 1, 2],
                "twirling_strategy": "active-accum",
            },
        }
        model = ResultsMetadataModel.model_validate(metadata)
        assert model.backend == "some_backend"
        assert isinstance(model.input_options, InputOptionsModel)
        assert model.input_options.max_layers_to_learn == 4

    def test_missing_backend_field(self):
        """Test that missing backend field is rejected."""
        metadata = {
            "input_options": {
                "max_layers_to_learn": 4,
                "shots_per_randomization": 128,
                "num_randomizations": 32,
                "layer_pair_depths": [0, 1],
                "twirling_strategy": "active",
            },
        }
        with pytest.raises(ValidationError, match="Field required"):
            ResultsMetadataModel.model_validate(metadata)

    def test_missing_input_options_field(self):
        """Test that missing input_options field is rejected."""
        metadata = {"backend": "ibm_brisbane"}
        with pytest.raises(ValidationError, match="Field required"):
            ResultsMetadataModel.model_validate(metadata)


class TestLayerNoiseModelValidation:
    """Test LayerNoiseModel validation."""

    def _create_valid_pauli_lindblad_error(self) -> dict:
        """Helper to create a valid PauliLindbladError dict."""
        import numpy as np

        # Create a simple ndarray and encode it
        rates = np.array([0.1, 0.2, 0.3])
        buffer = BytesIO()
        np.save(buffer, rates)
        rates_data = buffer.getvalue()
        compressed = zlib.compress(rates_data)
        encoded = pybase64.b64encode(compressed).decode("utf-8")

        return {
            "__type__": "_json",
            "__module__": "qiskit_ibm_runtime.utils.noise_learner_result",
            "__class__": "PauliLindbladError",
            "__value__": {
                "generators": {
                    "__type__": "settings",
                    "__module__": "qiskit.quantum_info.operators.symplectic.pauli_list",
                    "__class__": "PauliList",
                    "__value__": {"data": ["IX", "IY", "IZ"]},
                },
                "rates": {"__type__": "ndarray", "__value__": encoded},
            },
        }

    def test_valid_layer_noise_with_error(self, valid_circuit_dict):
        """Test that valid LayerNoiseModel with error is accepted."""
        circuit_dict = valid_circuit_dict
        error_dict = self._create_valid_pauli_lindblad_error()

        layer_noise = {
            "circuit": circuit_dict,
            "qubits": [0, 1],
            "error": error_dict,
        }
        model = LayerNoiseModel.model_validate(layer_noise)
        assert model.qubits == [0, 1]
        assert model.error is not None
        assert isinstance(model.error, PauliLindbladErrorWrapperModel)

    def test_optional_error_field_none(self, valid_circuit_dict):
        """Test that error field can be None (optional)."""
        circuit_dict = valid_circuit_dict

        layer_noise = {
            "circuit": circuit_dict,
            "qubits": [0, 1],
            "error": None,
        }
        model = LayerNoiseModel.model_validate(layer_noise)
        assert model.qubits == [0, 1]
        assert model.error is None

    def test_optional_error_field_omitted(self, valid_circuit_dict):
        """Test that error field can be omitted (defaults to None)."""
        circuit_dict = valid_circuit_dict

        layer_noise = {
            "circuit": circuit_dict,
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

    def test_missing_required_qubits_field(self, valid_circuit_dict):
        """Test that missing qubits field is rejected."""
        circuit_dict = valid_circuit_dict
        layer_noise = {"circuit": circuit_dict}
        with pytest.raises(ValidationError, match="Field required"):
            LayerNoiseModel.model_validate(layer_noise)


class TestResultsModelValidation:
    """Test ResultsModel validation."""

    def _create_valid_layer_noise_wrapper(self, valid_circuit_dict) -> dict:
        """Helper to create a valid LayerNoiseWrapperModel dict."""
        return {
            "__type__": "_json",
            "__module__": "qiskit_ibm_runtime.utils.noise_learner_result",
            "__class__": "LayerError",
            "__value__": {
                "circuit": valid_circuit_dict,
                "qubits": [0, 1],
                "error": None,
            },
        }

    def _create_valid_metadata(self) -> dict:
        """Helper to create valid metadata dict."""
        return {
            "backend": "ibm_brisbane",
            "input_options": {
                "max_layers_to_learn": 4,
                "shots_per_randomization": 128,
                "num_randomizations": 32,
                "layer_pair_depths": [0, 1, 2],
                "twirling_strategy": "active-accum",
            },
        }

    def test_valid_results_model(self, valid_circuit_dict):
        """Test that valid ResultsModel is accepted."""
        layer_noise = self._create_valid_layer_noise_wrapper(valid_circuit_dict)
        metadata = self._create_valid_metadata()

        results = {
            "schema_version": "v0.1",
            "data": [layer_noise],
            "metadata": metadata,
        }
        model = ResultsModel.model_validate(results)
        assert model.schema_version == "v0.1"
        assert len(model.data) == 1
        assert isinstance(model.data[0], LayerNoiseWrapperModel)
        assert isinstance(model.metadata, ResultsMetadataModel)

    def test_schema_version_default(self, valid_circuit_dict):
        """Test that schema_version has default value of 'v0.1'."""
        layer_noise = self._create_valid_layer_noise_wrapper(valid_circuit_dict)
        metadata = self._create_valid_metadata()

        results = {
            "data": [layer_noise],
            "metadata": metadata,
        }
        model = ResultsModel.model_validate(results)
        assert model.schema_version == "v0.1"

    def test_invalid_schema_version(self, valid_circuit_dict):
        """Test that invalid schema_version is rejected."""
        layer_noise = self._create_valid_layer_noise_wrapper(valid_circuit_dict)
        metadata = self._create_valid_metadata()

        results = {
            "schema_version": "v0.2",
            "data": [layer_noise],
            "metadata": metadata,
        }
        with pytest.raises(ValidationError, match="Input should be 'v0.1'"):
            ResultsModel.model_validate(results)

    def test_missing_data_field(self):
        """Test that missing data field is rejected."""
        metadata = self._create_valid_metadata()

        results = {
            "metadata": metadata,
        }
        with pytest.raises(ValidationError, match="Field required"):
            ResultsModel.model_validate(results)

    def test_missing_metadata_field(self, valid_circuit_dict):
        """Test that missing metadata field is rejected."""
        layer_noise = self._create_valid_layer_noise_wrapper(valid_circuit_dict)

        results = {
            "data": [layer_noise],
        }
        with pytest.raises(ValidationError, match="Field required"):
            ResultsModel.model_validate(results)
