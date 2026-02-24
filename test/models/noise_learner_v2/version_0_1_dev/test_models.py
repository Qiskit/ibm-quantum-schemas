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

    def test_missing_options_field(self, valid_typed_qpy_circuit_dict_v13):
        """Test that missing options field is rejected."""
        params = {"circuits": [valid_typed_qpy_circuit_dict_v13]}
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
