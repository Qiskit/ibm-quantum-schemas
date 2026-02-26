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

"""Validation tests for models.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.models.noise_learner_v2.version_0_1_dev.models import (
    LayerNoiseWrapperModel,
    ParamsModel,
    ResultsMetadataModel,
    ResultsModel,
    TypedQpyCircuitModelV13to17,
)


class TestParamsModelValidation:
    """Test ParamsModel validation."""

    def test_valid_params_model(self, valid_typed_qpy_circuit_dict_v13):
        """Test that valid params are accepted."""
        params = {
            "circuits": [valid_typed_qpy_circuit_dict_v13],
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

    def test_empty_circuits_list(self):
        """Test that empty circuits list is accepted."""
        params = {"circuits": [], "options": {}}
        model = ParamsModel.model_validate(params)
        assert len(model.circuits) == 0

    def test_multiple_circuits(self, valid_typed_qpy_circuit_dict_v13):
        """Test that multiple circuits are accepted."""
        params = {
            "circuits": [
                valid_typed_qpy_circuit_dict_v13,
                valid_typed_qpy_circuit_dict_v13,
                valid_typed_qpy_circuit_dict_v13,
            ],
            "options": {},
        }
        model = ParamsModel.model_validate(params)
        assert len(model.circuits) == 3
        assert isinstance(model.circuits[0], TypedQpyCircuitModelV13to17)

    def test_qasm_circuits(self):
        """Test that multiple circuits are accepted."""
        params = {
            "circuits": ["OPENQASM 3.0; qubit q; x q;"],
            "options": {},
        }
        model = ParamsModel.model_validate(params)
        assert len(model.circuits) == 1
        assert isinstance(model.circuits[0], str)

    def test_required_params_only(self):
        """Test when only required parameters are specified (circuits only, no options)."""
        params = {"circuits": []}
        model = ParamsModel.model_validate(params)
        assert model.circuits == []

    def test_optional_params(self, valid_typed_qpy_circuit_dict_v13):
        """Test passing both required and optional parameters."""
        params = {
            "circuits": [],
            "schema_version": "v0.1",
            "version": 2,
            "options": {},
        }
        ParamsModel.model_validate(params)

    def test_version_none(self, valid_typed_qpy_circuit_dict_v13):
        """Test ensuring that in addition to 2 Noise learner also accepts None version."""
        params = {
            "circuits": [],
            "version": None,
        }
        ParamsModel.model_validate(params)

    def test_extra_params(self):
        """Test passing extra parameters."""
        params = {"circuits": [], "options": {}, "foo": "bar"}
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            ParamsModel.model_validate(params)

    def test_extra_options(self):
        """Test passing extra options."""
        params = {"circuits": [], "options": {"foo": "bar"}}
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            ParamsModel.model_validate(params)

    @pytest.mark.parametrize(
        "bad_params",
        [
            {"circuits": "foo"},
            {"options": -1},
        ],
    )
    def test_invalid_param_type(self, bad_params):
        """Test invalid parameter types."""
        params = {"circuits": [], "options": {}}
        params.update(bad_params)
        bad_key = list(bad_params.keys())[0]
        with pytest.raises(ValidationError, match=bad_key):
            ParamsModel.model_validate(params)

    @pytest.mark.parametrize("num_circs", [1, 2, 5])
    def test_valid_circuits(self, valid_typed_qpy_circuit_dict_v13, num_circs):
        """Test a list of circuits."""
        params = {
            "circuits": [valid_typed_qpy_circuit_dict_v13] * num_circs,
            "options": {},
        }
        model = ParamsModel.model_validate(params)
        assert len(model.circuits) == num_circs

    def test_simulator_options(self):
        """Test simulator options."""
        params = {
            "circuits": [],
            "options": {"simulator": {"coupling_map": [[0, 1], [1, 2]]}},
        }
        model = ParamsModel.model_validate(params)
        assert model.options.simulator is not None
        assert model.options.simulator.coupling_map == [[0, 1], [1, 2]]

    def test_simulator_none(self):
        """Test simulator options with none"""
        params = {
            "circuits": [],
            "options": {"simulator": {"coupling_map": [[0, 1], [1, 2]], "seed_simulator": None}},
        }
        model = ParamsModel.model_validate(params)
        assert model.options.simulator is not None
        assert model.options.simulator.coupling_map == [[0, 1], [1, 2]]
        assert model.options.simulator.seed_simulator is None


class TestResultsModelValidation:
    """Test ResultsModel validation."""

    def test_valid_results_model(self, valid_layer_noise_wrapper, valid_metadata):
        """Test that valid ResultsModel is accepted."""
        results = {
            "schema_version": "v0.1",
            "data": [valid_layer_noise_wrapper],
            "metadata": valid_metadata,
        }
        model = ResultsModel.model_validate(results)
        assert model.schema_version == "v0.1"
        assert len(model.data) == 1
        assert isinstance(model.data[0], LayerNoiseWrapperModel)
        assert isinstance(model.metadata, ResultsMetadataModel)

    def test_schema_version_default(self, valid_layer_noise_wrapper, valid_metadata):
        """Test that schema_version has default value of 'v0.1'."""
        results = {
            "data": [valid_layer_noise_wrapper],
            "metadata": valid_metadata,
        }
        model = ResultsModel.model_validate(results)
        assert model.schema_version == "v0.1"

    def test_invalid_schema_version(self, valid_layer_noise_wrapper, valid_metadata):
        """Test that invalid schema_version is rejected."""
        results = {
            "schema_version": "v0.2",
            "data": [valid_layer_noise_wrapper],
            "metadata": valid_metadata,
        }
        with pytest.raises(ValidationError, match="Input should be 'v0.1'"):
            ResultsModel.model_validate(results)

    def test_missing_data_field(self, valid_metadata):
        """Test that missing data field is rejected."""
        results = {
            "metadata": valid_metadata,
        }
        with pytest.raises(ValidationError, match="Field required"):
            ResultsModel.model_validate(results)

    def test_missing_metadata_field(self, valid_layer_noise_wrapper):
        """Test that missing metadata field is rejected."""
        results = {
            "data": [valid_layer_noise_wrapper],
        }
        with pytest.raises(ValidationError, match="Field required"):
            ResultsModel.model_validate(results)
