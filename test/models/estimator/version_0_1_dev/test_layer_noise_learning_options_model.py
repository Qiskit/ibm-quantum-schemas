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

"""Validation tests for layer_noise_learning_options_model.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.models.estimator.version_0_1_dev.layer_noise_learning_options_model import (
    LayerNoiseLearningOptionsModel,
)


class TestLayerNoiseLearningOptionsModelValidation:
    """Test LayerNoiseLearningOptionsModel validation."""

    def test_valid_options_with_defaults(self):
        """Test that options with default values are accepted."""
        model = LayerNoiseLearningOptionsModel.model_validate({})
        assert model.max_layers_to_learn == 4
        assert model.shots_per_randomization == 128
        assert model.num_randomizations == 32
        assert model.layer_pair_depths == [0, 1, 2, 4, 16, 32]

    def test_valid_options_with_custom_values(self):
        """Test that custom option values are accepted."""
        options = {
            "max_layers_to_learn": 10,
            "shots_per_randomization": 256,
            "num_randomizations": 64,
            "layer_pair_depths": [0, 2, 4, 8],
        }
        model = LayerNoiseLearningOptionsModel.model_validate(options)
        assert model.max_layers_to_learn == 10
        assert model.shots_per_randomization == 256
        assert model.num_randomizations == 64
        assert model.layer_pair_depths == [0, 2, 4, 8]

    def test_none_max_layers_to_learn(self):
        """Test that None is accepted for max_layers_to_learn."""
        options = {"max_layers_to_learn": None}
        model = LayerNoiseLearningOptionsModel.model_validate(options)
        assert model.max_layers_to_learn is None

    def test_zero_max_layers_to_learn(self):
        """Test that zero max_layers_to_learn is accepted."""
        options = {"max_layers_to_learn": 0}
        model = LayerNoiseLearningOptionsModel.model_validate(options)
        assert model.max_layers_to_learn == 0

    def test_negative_max_layers_to_learn(self):
        """Test that negative max_layers_to_learn is rejected."""
        options = {"max_layers_to_learn": -1}
        with pytest.raises(ValidationError, match="greater than or equal to 0"):
            LayerNoiseLearningOptionsModel.model_validate(options)

    def test_zero_shots_per_randomization(self):
        """Test that zero shots_per_randomization is rejected."""
        options = {"shots_per_randomization": 0}
        with pytest.raises(ValidationError, match="greater than or equal to 1"):
            LayerNoiseLearningOptionsModel.model_validate(options)

    def test_negative_shots_per_randomization(self):
        """Test that negative shots_per_randomization is rejected."""
        options = {"shots_per_randomization": -1}
        with pytest.raises(ValidationError, match="greater than or equal to 1"):
            LayerNoiseLearningOptionsModel.model_validate(options)

    def test_one_shots_per_randomization(self):
        """Test that shots_per_randomization of 1 is accepted."""
        options = {"shots_per_randomization": 1}
        model = LayerNoiseLearningOptionsModel.model_validate(options)
        assert model.shots_per_randomization == 1

    def test_zero_num_randomizations(self):
        """Test that zero num_randomizations is rejected."""
        options = {"num_randomizations": 0}
        with pytest.raises(ValidationError, match="greater than or equal to 1"):
            LayerNoiseLearningOptionsModel.model_validate(options)

    def test_negative_num_randomizations(self):
        """Test that negative num_randomizations is rejected."""
        options = {"num_randomizations": -1}
        with pytest.raises(ValidationError, match="greater than or equal to 1"):
            LayerNoiseLearningOptionsModel.model_validate(options)

    def test_one_num_randomizations(self):
        """Test that num_randomizations of 1 is accepted."""
        options = {"num_randomizations": 1}
        model = LayerNoiseLearningOptionsModel.model_validate(options)
        assert model.num_randomizations == 1

    def test_empty_layer_pair_depths(self):
        """Test that empty layer_pair_depths list is accepted."""
        options = {"layer_pair_depths": []}
        model = LayerNoiseLearningOptionsModel.model_validate(options)
        assert model.layer_pair_depths == []

    def test_custom_layer_pair_depths(self):
        """Test that custom layer_pair_depths are accepted."""
        options = {"layer_pair_depths": [1, 3, 5, 7, 9]}
        model = LayerNoiseLearningOptionsModel.model_validate(options)
        assert model.layer_pair_depths == [1, 3, 5, 7, 9]

    def test_extra_fields_forbidden(self):
        """Test that extra fields are forbidden."""
        options = {"extra_field": "not allowed"}
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            LayerNoiseLearningOptionsModel.model_validate(options)
