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

"""Validation tests for zne_options_model.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.models.estimator.version_0_1_dev.zne_options_model import (
    ZneOptionsModel,
)


class TestZneOptionsModelValidation:
    """Test ZneOptionsModel validation."""

    def test_valid_options_with_defaults(self):
        """Test that options with default values are accepted."""
        model = ZneOptionsModel.model_validate({})
        assert model.amplifier == "gate_folding"
        assert model.noise_factors == (1, 3, 5)
        assert model.extrapolator == ("exponential", "linear", "fallback")
        assert model.extrapolated_noise_factors is None

    def test_valid_options_with_custom_values(self):
        """Test that custom option values are accepted."""
        options = {
            "amplifier": "pea",
            "noise_factors": [1, 2, 3, 4],
            "extrapolator": "linear",
            "extrapolated_noise_factors": [0, 1, 2],
        }
        model = ZneOptionsModel.model_validate(options)
        assert model.amplifier == "pea"
        assert model.noise_factors == [1, 2, 3, 4]
        assert model.extrapolator == "linear"
        assert model.extrapolated_noise_factors == [0, 1, 2]

    def test_invalid_amplifier(self):
        """Test that invalid amplifier is rejected."""
        options = {"amplifier": "invalid"}
        with pytest.raises(ValidationError):
            ZneOptionsModel.model_validate(options)

    def test_noise_factors_less_than_one(self):
        """Test that noise_factors less than 1 are rejected."""
        options = {"noise_factors": [0.5, 1, 2]}
        with pytest.raises(ValidationError, match="must all be >= 1"):
            ZneOptionsModel.model_validate(options)

    def test_valid_extrapolator_double_exponential(self):
        """Test that 'double_exponential' extrapolator is accepted."""
        options = {"extrapolator": "double_exponential", "noise_factors": [1, 2, 3, 4, 5]}
        model = ZneOptionsModel.model_validate(options)
        assert model.extrapolator == "double_exponential"

    def test_valid_extrapolator_polynomial_degree_7(self):
        """Test that 'polynomial_degree_7' extrapolator is accepted."""
        options = {
            "extrapolator": "polynomial_degree_7",
            "noise_factors": [1, 2, 3, 4, 5, 6, 7, 8],
        }
        model = ZneOptionsModel.model_validate(options)
        assert model.extrapolator == "polynomial_degree_7"

    def test_invalid_extrapolator(self):
        """Test that invalid extrapolator is rejected."""
        options = {"extrapolator": "invalid"}
        with pytest.raises(ValidationError):
            ZneOptionsModel.model_validate(options)

    def test_multiple_extrapolators(self):
        """Test that multiple extrapolators are accepted."""
        options = {"extrapolator": ["exponential", "linear", "fallback"]}
        model = ZneOptionsModel.model_validate(options)
        assert model.extrapolator == ["exponential", "linear", "fallback"]

    def test_insufficient_noise_factors_for_linear(self):
        """Test that insufficient noise_factors for linear extrapolator is rejected."""
        options = {"extrapolator": "linear", "noise_factors": [1]}
        with pytest.raises(ValidationError, match="linear requires at least 2 noise_factors"):
            ZneOptionsModel.model_validate(options)

    def test_insufficient_noise_factors_for_exponential(self):
        """Test that insufficient noise_factors for exponential extrapolator is rejected."""
        options = {"extrapolator": "exponential", "noise_factors": [1]}
        with pytest.raises(ValidationError, match="exponential requires at least 2 noise_factors"):
            ZneOptionsModel.model_validate(options)

    def test_insufficient_noise_factors_for_double_exponential(self):
        """Test that insufficient noise_factors for double_exponential is rejected."""
        options = {"extrapolator": "double_exponential", "noise_factors": [1, 2, 3]}
        with pytest.raises(
            ValidationError, match="double_exponential requires at least 4 noise_factors"
        ):
            ZneOptionsModel.model_validate(options)

    def test_insufficient_noise_factors_for_polynomial_degree_3(self):
        """Test that insufficient noise_factors for polynomial_degree_3 is rejected."""
        options = {"extrapolator": "polynomial_degree_3", "noise_factors": [1, 2, 3]}
        with pytest.raises(
            ValidationError, match="polynomial_degree_3 requires at least 4 noise_factors"
        ):
            ZneOptionsModel.model_validate(options)

    def test_sufficient_noise_factors_for_fallback(self):
        """Test that fallback only requires 1 noise_factor."""
        options = {"extrapolator": "fallback", "noise_factors": [1]}
        model = ZneOptionsModel.model_validate(options)
        assert model.extrapolator == "fallback"
        assert model.noise_factors == [1]

    def test_empty_extrapolated_noise_factors(self):
        """Test that empty extrapolated_noise_factors is accepted."""
        options = {"noise_factors": [1, 2], "extrapolated_noise_factors": []}
        model = ZneOptionsModel.model_validate(options)
        assert model.extrapolated_noise_factors == []

    def test_multiple_extrapolators_insufficient_noise_factors(self):
        """Test that multiple extrapolators with insufficient noise_factors is rejected."""
        options = {
            "extrapolator": ["exponential", "polynomial_degree_5"],
            "noise_factors": [1, 2, 3],
        }
        with pytest.raises(
            ValidationError, match="polynomial_degree_5 requires at least 6 noise_factors"
        ):
            ZneOptionsModel.model_validate(options)

    def test_empty_extrapolator_sequence(self):
        """Test that empty extrapolator sequence is rejected."""
        options = {"extrapolator": []}
        with pytest.raises(ValidationError, match="extrapolator sequence cannot be empty"):
            ZneOptionsModel.model_validate(options)
