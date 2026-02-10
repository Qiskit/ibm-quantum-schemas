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

"""Validation tests for results_metadata_model.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.models.noise_learner_v2.version_0_1_dev.results_metadata_model import (
    InputOptionsModel,
    ResultsMetadataModel,
)


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
