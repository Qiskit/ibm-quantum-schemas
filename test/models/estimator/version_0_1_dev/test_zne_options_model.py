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
        assert model.extrapolator == ("exponential", "linear")
        assert model.extrapolated_noise_factors == (0, 1, 3, 5)

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

    def test_valid_amplifier_gate_folding(self):
        """Test that 'gate_folding' amplifier is accepted."""
        options = {"amplifier": "gate_folding"}
        model = ZneOptionsModel.model_validate(options)
        assert model.amplifier == "gate_folding"

    def test_valid_amplifier_gate_folding_front(self):
        """Test that 'gate_folding_front' amplifier is accepted."""
        options = {"amplifier": "gate_folding_front"}
        model = ZneOptionsModel.model_validate(options)
        assert model.amplifier == "gate_folding_front"

    def test_valid_amplifier_gate_folding_back(self):
        """Test that 'gate_folding_back' amplifier is accepted."""
        options = {"amplifier": "gate_folding_back"}
        model = ZneOptionsModel.model_validate(options)
        assert model.amplifier == "gate_folding_back"

    def test_valid_amplifier_pea(self):
        """Test that 'pea' amplifier is accepted."""
        options = {"amplifier": "pea"}
        model = ZneOptionsModel.model_validate(options)
        assert model.amplifier == "pea"
        # PEA should set default noise_factors to (1, 1.5, 2, 2.5, 3)
        assert model.noise_factors == (1, 1.5, 2, 2.5, 3)

    def test_invalid_amplifier(self):
        """Test that invalid amplifier is rejected."""
        options = {"amplifier": "invalid"}
        with pytest.raises(ValidationError):
            ZneOptionsModel.model_validate(options)

    def test_none_noise_factors_with_gate_folding(self):
        """Test that None noise_factors defaults correctly for gate_folding."""
        options = {"amplifier": "gate_folding", "noise_factors": None}
        model = ZneOptionsModel.model_validate(options)
        assert model.noise_factors == (1, 3, 5)

    def test_none_noise_factors_with_pea(self):
        """Test that None noise_factors defaults correctly for pea."""
        options = {"amplifier": "pea", "noise_factors": None}
        model = ZneOptionsModel.model_validate(options)
        assert model.noise_factors == (1, 1.5, 2, 2.5, 3)

    def test_noise_factors_less_than_one(self):
        """Test that noise_factors less than 1 are rejected."""
        options = {"noise_factors": [0.5, 1, 2]}
        with pytest.raises(ValidationError, match="must all be >= 1"):
            ZneOptionsModel.model_validate(options)

    def test_noise_factors_with_one(self):
        """Test that noise_factors with 1 are accepted."""
        options = {"noise_factors": [1, 2, 3]}
        model = ZneOptionsModel.model_validate(options)
        assert model.noise_factors == [1, 2, 3]

    def test_valid_extrapolator_linear(self):
        """Test that 'linear' extrapolator is accepted."""
        options = {"extrapolator": "linear"}
        model = ZneOptionsModel.model_validate(options)
        assert model.extrapolator == "linear"

    def test_valid_extrapolator_exponential(self):
        """Test that 'exponential' extrapolator is accepted."""
        options = {"extrapolator": "exponential"}
        model = ZneOptionsModel.model_validate(options)
        assert model.extrapolator == "exponential"

    def test_valid_extrapolator_double_exponential(self):
        """Test that 'double_exponential' extrapolator is accepted."""
        options = {"extrapolator": "double_exponential", "noise_factors": [1, 2, 3, 4, 5]}
        model = ZneOptionsModel.model_validate(options)
        assert model.extrapolator == "double_exponential"

    def test_valid_extrapolator_polynomial_degree_1(self):
        """Test that 'polynomial_degree_1' extrapolator is accepted."""
        options = {"extrapolator": "polynomial_degree_1"}
        model = ZneOptionsModel.model_validate(options)
        assert model.extrapolator == "polynomial_degree_1"

    def test_valid_extrapolator_polynomial_degree_7(self):
        """Test that 'polynomial_degree_7' extrapolator is accepted."""
        options = {
            "extrapolator": "polynomial_degree_7",
            "noise_factors": [1, 2, 3, 4, 5, 6, 7, 8],
        }
        model = ZneOptionsModel.model_validate(options)
        assert model.extrapolator == "polynomial_degree_7"

    def test_valid_extrapolator_fallback(self):
        """Test that 'fallback' extrapolator is accepted."""
        options = {"extrapolator": "fallback", "noise_factors": [1]}
        model = ZneOptionsModel.model_validate(options)
        assert model.extrapolator == "fallback"

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

    def test_extrapolated_noise_factors_default(self):
        """Test that extrapolated_noise_factors defaults correctly."""
        options = {"noise_factors": [1, 2, 3]}
        model = ZneOptionsModel.model_validate(options)
        assert model.extrapolated_noise_factors == (0, 1, 2, 3)

    def test_extrapolated_noise_factors_custom(self):
        """Test that custom extrapolated_noise_factors are accepted."""
        options = {
            "noise_factors": [1, 2, 3],
            "extrapolated_noise_factors": [0, 0.5, 1, 1.5, 2],
        }
        model = ZneOptionsModel.model_validate(options)
        assert model.extrapolated_noise_factors == [0, 0.5, 1, 1.5, 2]

    def test_empty_extrapolated_noise_factors(self):
        """Test that empty extrapolated_noise_factors defaults correctly."""
        options = {"noise_factors": [1, 2], "extrapolated_noise_factors": []}
        model = ZneOptionsModel.model_validate(options)
        assert model.extrapolated_noise_factors == (0, 1, 2)

    def test_extra_fields_forbidden(self):
        """Test that extra fields are forbidden."""
        options = {"extra_field": "not allowed"}
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            ZneOptionsModel.model_validate(options)

    def test_complex_valid_case(self):
        """Test a complex valid case with multiple options."""
        options = {
            "amplifier": "gate_folding_front",
            "noise_factors": [1, 2, 3, 4, 5],
            "extrapolator": ["exponential", "linear", "polynomial_degree_2"],
            "extrapolated_noise_factors": [0, 1, 2, 3, 4, 5, 6],
        }
        model = ZneOptionsModel.model_validate(options)
        assert model.amplifier == "gate_folding_front"
        assert model.noise_factors == [1, 2, 3, 4, 5]
        assert model.extrapolator == ["exponential", "linear", "polynomial_degree_2"]
        assert model.extrapolated_noise_factors == [0, 1, 2, 3, 4, 5, 6]

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

