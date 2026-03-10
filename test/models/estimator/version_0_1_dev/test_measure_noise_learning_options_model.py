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

"""Validation tests for measure_noise_learning_options_model.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.models.estimator.version_0_1_dev import (
    measure_noise_learning_options_model as mnl_options,
)

MeasureNoiseLearningOptionsModel = mnl_options.MeasureNoiseLearningOptionsModel


class TestMeasureNoiseLearningOptionsModelValidation:
    """Test MeasureNoiseLearningOptionsModel validation."""

    def test_valid_options_with_defaults(self):
        """Test that measure noise learning options with default values are accepted."""
        model = MeasureNoiseLearningOptionsModel.model_validate({})

        # Verify all default values
        assert model.num_randomizations == 32
        assert model.shots_per_randomization == "auto"

    def test_valid_options_with_custom_values(self):
        """Test that custom measure noise learning option values are accepted."""
        options = {
            "num_randomizations": 64,
            "shots_per_randomization": 256,
        }
        model = MeasureNoiseLearningOptionsModel.model_validate(options)
        assert model.num_randomizations == 64
        assert model.shots_per_randomization == 256

    def test_num_randomizations_positive_integer(self):
        """Test that positive integer num_randomizations is accepted."""
        options = {"num_randomizations": 128}
        model = MeasureNoiseLearningOptionsModel.model_validate(options)
        assert model.num_randomizations == 128

    def test_num_randomizations_one(self):
        """Test that num_randomizations of 1 is accepted."""
        options = {"num_randomizations": 1}
        model = MeasureNoiseLearningOptionsModel.model_validate(options)
        assert model.num_randomizations == 1

    def test_num_randomizations_zero_rejected(self):
        """Test that num_randomizations of 0 is rejected."""
        options = {"num_randomizations": 0}
        with pytest.raises(ValidationError, match="greater than or equal to 1"):
            MeasureNoiseLearningOptionsModel.model_validate(options)

    def test_num_randomizations_negative_rejected(self):
        """Test that negative num_randomizations is rejected."""
        options = {"num_randomizations": -1}
        with pytest.raises(ValidationError, match="greater than or equal to 1"):
            MeasureNoiseLearningOptionsModel.model_validate(options)

    def test_shots_per_randomization_auto(self):
        """Test that shots_per_randomization can be 'auto'."""
        options = {"shots_per_randomization": "auto"}
        model = MeasureNoiseLearningOptionsModel.model_validate(options)
        assert model.shots_per_randomization == "auto"

    def test_shots_per_randomization_positive_integer(self):
        """Test that positive integer shots_per_randomization is accepted."""
        options = {"shots_per_randomization": 512}
        model = MeasureNoiseLearningOptionsModel.model_validate(options)
        assert model.shots_per_randomization == 512

    def test_shots_per_randomization_one(self):
        """Test that shots_per_randomization of 1 is accepted."""
        options = {"shots_per_randomization": 1}
        model = MeasureNoiseLearningOptionsModel.model_validate(options)
        assert model.shots_per_randomization == 1

    def test_shots_per_randomization_zero_rejected(self):
        """Test that shots_per_randomization of 0 is rejected."""
        options = {"shots_per_randomization": 0}
        with pytest.raises(ValidationError, match="greater than or equal to 1"):
            MeasureNoiseLearningOptionsModel.model_validate(options)

    def test_shots_per_randomization_negative_rejected(self):
        """Test that negative shots_per_randomization is rejected."""
        options = {"shots_per_randomization": -1}
        with pytest.raises(ValidationError, match="greater than or equal to 1"):
            MeasureNoiseLearningOptionsModel.model_validate(options)

    def test_extra_fields_forbidden(self):
        """Test that extra fields are forbidden."""
        options = {"extra_field": "not allowed"}
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            MeasureNoiseLearningOptionsModel.model_validate(options)
