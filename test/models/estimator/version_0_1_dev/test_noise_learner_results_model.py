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

"""Validation tests for noise_learner_results_model.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.models.estimator.version_0_1_dev.noise_learner_results_model import (
    NoiseLearnerInputOptionsModel,
    NoiseLearnerResultMetadataModel,
    NoiseLearnerResultModel,
    NoiseLearnerResultWrapperModel,
)


class TestNoiseLearnerInputOptionsModelValidation:
    """Test NoiseLearnerInputOptionsModel validation."""

    def test_valid_input_options(self):
        """Test that valid input options are accepted."""
        options = {
            "max_layers_to_learn": 4,
            "shots_per_randomization": 128,
            "num_randomizations": 32,
            "layer_pair_depths": [0, 1, 2, 4, 16, 32],
            "twirling_strategy": "active-accum",
        }
        model = NoiseLearnerInputOptionsModel.model_validate(options)
        assert model.max_layers_to_learn == 4
        assert model.shots_per_randomization == 128
        assert model.num_randomizations == 32
        assert model.layer_pair_depths == [0, 1, 2, 4, 16, 32]
        assert model.twirling_strategy == "active-accum"

    def test_none_max_layers_to_learn(self):
        """Test that None is accepted for max_layers_to_learn."""
        options = {
            "max_layers_to_learn": None,
            "shots_per_randomization": 128,
            "num_randomizations": 32,
            "layer_pair_depths": [0, 1, 2],
            "twirling_strategy": "active",
        }
        model = NoiseLearnerInputOptionsModel.model_validate(options)
        assert model.max_layers_to_learn is None

    def test_valid_twirling_strategies(self):
        """Test that all valid twirling strategies are accepted."""
        strategies = ["active", "active-circuit", "active-accum", "all"]
        for strategy in strategies:
            options = {
                "max_layers_to_learn": 4,
                "shots_per_randomization": 128,
                "num_randomizations": 32,
                "layer_pair_depths": [0, 1, 2],
                "twirling_strategy": strategy,
            }
            model = NoiseLearnerInputOptionsModel.model_validate(options)
            assert model.twirling_strategy == strategy

    def test_invalid_twirling_strategy(self):
        """Test that invalid twirling strategy is rejected."""
        options = {
            "max_layers_to_learn": 4,
            "shots_per_randomization": 128,
            "num_randomizations": 32,
            "layer_pair_depths": [0, 1, 2],
            "twirling_strategy": "invalid",
        }
        with pytest.raises(ValidationError):
            NoiseLearnerInputOptionsModel.model_validate(options)

    def test_missing_required_fields(self):
        """Test that missing required fields are rejected."""
        with pytest.raises(ValidationError, match="Field required"):
            NoiseLearnerInputOptionsModel.model_validate({})


class TestNoiseLearnerResultMetadataModelValidation:
    """Test NoiseLearnerResultMetadataModel validation."""

    def test_valid_metadata(self):
        """Test that valid metadata is accepted."""
        metadata = {
            "backend": "ibm_brisbane",
            "input_options": {
                "max_layers_to_learn": 4,
                "shots_per_randomization": 128,
                "num_randomizations": 32,
                "layer_pair_depths": [0, 1, 2],
                "twirling_strategy": "active-accum",
            },
        }
        model = NoiseLearnerResultMetadataModel.model_validate(metadata)
        assert model.backend == "ibm_brisbane"
        assert isinstance(model.input_options, NoiseLearnerInputOptionsModel)
        assert model.input_options.max_layers_to_learn == 4
        assert model.input_options.shots_per_randomization == 128
        assert model.input_options.num_randomizations == 32
        assert model.input_options.layer_pair_depths == [0, 1, 2]
        assert model.input_options.twirling_strategy == "active-accum"

    def test_missing_backend(self):
        """Test that missing backend field is rejected."""
        metadata = {
            "input_options": {
                "max_layers_to_learn": 4,
                "shots_per_randomization": 128,
                "num_randomizations": 32,
                "layer_pair_depths": [0, 1, 2],
                "twirling_strategy": "active",
            },
        }
        with pytest.raises(ValidationError, match="Field required"):
            NoiseLearnerResultMetadataModel.model_validate(metadata)

    def test_missing_input_options(self):
        """Test that missing input_options field is rejected."""
        metadata = {"backend": "ibm_brisbane"}
        with pytest.raises(ValidationError, match="Field required"):
            NoiseLearnerResultMetadataModel.model_validate(metadata)


class TestNoiseLearnerResultModelValidation:
    """Test NoiseLearnerResultModel validation."""

    def test_valid_results_with_data(self, valid_layer_noise_wrapper):
        """Test that valid results with data are accepted."""
        results = {
            "data": [valid_layer_noise_wrapper],
            "metadata": {
                "backend": "ibm_brisbane",
                "input_options": {
                    "max_layers_to_learn": 4,
                    "shots_per_randomization": 128,
                    "num_randomizations": 32,
                    "layer_pair_depths": [0, 1, 2],
                    "twirling_strategy": "active-accum",
                },
            },
        }
        model = NoiseLearnerResultModel.model_validate(results)
        assert len(model.data) == 1
        assert isinstance(model.metadata, NoiseLearnerResultMetadataModel)
        assert model.metadata.backend == "ibm_brisbane"
        assert isinstance(model.metadata.input_options, NoiseLearnerInputOptionsModel)
        assert model.metadata.input_options.max_layers_to_learn == 4
        assert model.metadata.input_options.shots_per_randomization == 128
        assert model.metadata.input_options.num_randomizations == 32
        assert model.metadata.input_options.layer_pair_depths == [0, 1, 2]
        assert model.metadata.input_options.twirling_strategy == "active-accum"

    def test_valid_results_with_empty_data(self):
        """Test that valid results with empty data are accepted."""
        results = {
            "data": [],
            "metadata": {
                "backend": "ibm_brisbane",
                "input_options": {
                    "max_layers_to_learn": 4,
                    "shots_per_randomization": 128,
                    "num_randomizations": 32,
                    "layer_pair_depths": [0, 1, 2],
                    "twirling_strategy": "active",
                },
            },
        }
        model = NoiseLearnerResultModel.model_validate(results)
        assert len(model.data) == 0

    def test_missing_data_field(self):
        """Test that missing data field is rejected."""
        results = {
            "metadata": {
                "backend": "ibm_brisbane",
                "input_options": {
                    "max_layers_to_learn": 4,
                    "shots_per_randomization": 128,
                    "num_randomizations": 32,
                    "layer_pair_depths": [0, 1, 2],
                    "twirling_strategy": "active",
                },
            },
        }
        with pytest.raises(ValidationError, match="Field required"):
            NoiseLearnerResultModel.model_validate(results)

    def test_missing_metadata_field(self):
        """Test that missing metadata field is rejected."""
        results = {
            "data": [],
        }
        with pytest.raises(ValidationError, match="Field required"):
            NoiseLearnerResultModel.model_validate(results)


class TestNoiseLearnerResultWrapperModelValidation:
    """Test NoiseLearnerResultWrapperModel validation."""

    def test_valid_wrapper_with_data(self, valid_layer_noise_wrapper):
        """Test that valid wrapper with data is accepted."""
        wrapper = {
            "__type__": "NoiseLearnerResult",
            "__value__": {
                "data": [valid_layer_noise_wrapper],
                "metadata": {
                    "backend": "ibm_brisbane",
                    "input_options": {
                        "max_layers_to_learn": 4,
                        "shots_per_randomization": 128,
                        "num_randomizations": 32,
                        "layer_pair_depths": [0, 1, 2],
                        "twirling_strategy": "active-accum",
                    },
                },
            },
        }
        model = NoiseLearnerResultWrapperModel.model_validate(wrapper)
        assert model.type_ == "NoiseLearnerResult"
        assert isinstance(model.value_, NoiseLearnerResultModel)
        assert len(model.value_.data) == 1
        assert isinstance(model.value_.metadata, NoiseLearnerResultMetadataModel)
        assert model.value_.metadata.backend == "ibm_brisbane"
