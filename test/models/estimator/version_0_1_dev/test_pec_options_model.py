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

"""Validation tests for pec_options_model.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.models.estimator.version_0_1_dev.pec_options_model import (
    PecOptionsModel,
)


class TestPecOptionsModelValidation:
    """Test PecOptionsModel validation."""

    def test_valid_options_with_defaults(self):
        """Test that options with default values are accepted."""
        model = PecOptionsModel.model_validate({})
        assert model.max_overhead == 100.0
        assert model.noise_gain == "auto"

    def test_valid_options_with_custom_values(self):
        """Test that custom option values are accepted."""
        options = {
            "max_overhead": 50.0,
            "noise_gain": 0.5,
        }
        model = PecOptionsModel.model_validate(options)
        assert model.max_overhead == 50.0
        assert model.noise_gain == 0.5

    def test_none_max_overhead(self):
        """Test that None is accepted for max_overhead."""
        options = {"max_overhead": None}
        model = PecOptionsModel.model_validate(options)
        assert model.max_overhead is None

    def test_zero_max_overhead(self):
        """Test that zero max_overhead is rejected."""
        options = {"max_overhead": 0.0}
        with pytest.raises(ValidationError, match="greater than 0"):
            PecOptionsModel.model_validate(options)

    def test_negative_max_overhead(self):
        """Test that negative max_overhead is rejected."""
        options = {"max_overhead": -1.0}
        with pytest.raises(ValidationError, match="greater than 0"):
            PecOptionsModel.model_validate(options)

    def test_positive_max_overhead(self):
        """Test that positive max_overhead is accepted."""
        options = {"max_overhead": 200.0}
        model = PecOptionsModel.model_validate(options)
        assert model.max_overhead == 200.0

    def test_small_positive_max_overhead(self):
        """Test that small positive max_overhead is accepted."""
        options = {"max_overhead": 0.001}
        model = PecOptionsModel.model_validate(options)
        assert model.max_overhead == 0.001

    def test_noise_gain_auto(self):
        """Test that 'auto' is accepted for noise_gain."""
        options = {"noise_gain": "auto"}
        model = PecOptionsModel.model_validate(options)
        assert model.noise_gain == "auto"

    def test_noise_gain_zero(self):
        """Test that zero noise_gain is accepted."""
        options = {"noise_gain": 0.0}
        model = PecOptionsModel.model_validate(options)
        assert model.noise_gain == 0.0

    def test_noise_gain_one(self):
        """Test that noise_gain of 1 is accepted."""
        options = {"noise_gain": 1.0}
        model = PecOptionsModel.model_validate(options)
        assert model.noise_gain == 1.0

    def test_noise_gain_between_zero_and_one(self):
        """Test that noise_gain between 0 and 1 is accepted."""
        options = {"noise_gain": 0.5}
        model = PecOptionsModel.model_validate(options)
        assert model.noise_gain == 0.5

    def test_noise_gain_greater_than_one(self):
        """Test that noise_gain greater than 1 is accepted."""
        options = {"noise_gain": 2.0}
        model = PecOptionsModel.model_validate(options)
        assert model.noise_gain == 2.0

    def test_negative_noise_gain(self):
        """Test that negative noise_gain is rejected."""
        options = {"noise_gain": -0.5}
        with pytest.raises(ValidationError, match="noise_gain must be >= 0"):
            PecOptionsModel.model_validate(options)

    def test_noise_gain_integer_zero(self):
        """Test that integer zero noise_gain is accepted."""
        options = {"noise_gain": 0}
        model = PecOptionsModel.model_validate(options)
        assert model.noise_gain == 0

    def test_noise_gain_integer_positive(self):
        """Test that positive integer noise_gain is accepted."""
        options = {"noise_gain": 2}
        model = PecOptionsModel.model_validate(options)
        assert model.noise_gain == 2

    def test_noise_gain_integer_negative(self):
        """Test that negative integer noise_gain is rejected."""
        options = {"noise_gain": -1}
        with pytest.raises(ValidationError, match="noise_gain must be >= 0"):
            PecOptionsModel.model_validate(options)

    def test_invalid_noise_gain_string(self):
        """Test that invalid string for noise_gain is rejected."""
        options = {"noise_gain": "invalid"}
        with pytest.raises(ValidationError):
            PecOptionsModel.model_validate(options)

    def test_extra_fields_forbidden(self):
        """Test that extra fields are forbidden."""
        options = {"extra_field": "not allowed"}
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            PecOptionsModel.model_validate(options)

    def test_combined_none_and_auto(self):
        """Test that None max_overhead and auto noise_gain are accepted."""
        options = {
            "max_overhead": None,
            "noise_gain": "auto",
        }
        model = PecOptionsModel.model_validate(options)
        assert model.max_overhead is None
        assert model.noise_gain == "auto"

# Made with Bob
