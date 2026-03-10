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

"""Validation tests for primitive_result_zne_metadata_model.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.models.estimator.version_0_1_dev.output.primitive_result_zne_metadata_model import (  # noqa: E501
    PrimitiveResultZneMetadataModel,
)


class TestPrimitiveResultZneMetadataModelValidation:
    """Test PrimitiveResultZneMetadataModel validation."""

    def test_valid_metadata_with_noise_factors(self):
        """Test that metadata with noise_factors is valid."""
        data = {"noise_factors": [1.0, 1.5, 2.0]}
        model = PrimitiveResultZneMetadataModel.model_validate(data)
        assert model.noise_factors == [1.0, 1.5, 2.0]
        assert model.extrapolator is None
        assert model.extrapolated_noise_factors is None

    def test_valid_metadata_with_all_fields(self):
        """Test that metadata with all fields is valid."""
        data = {
            "noise_factors": [1.0, 2.0, 3.0],
            "extrapolator": "exponential",
            "extrapolated_noise_factors": [0.0, 1.0, 2.0],
        }
        model = PrimitiveResultZneMetadataModel.model_validate(data)
        assert model.noise_factors == [1.0, 2.0, 3.0]
        assert model.extrapolator == "exponential"
        assert model.extrapolated_noise_factors == [0.0, 1.0, 2.0]

    def test_noise_factors_none(self):
        """Test that noise_factors can be None."""
        data = {"noise_factors": None}
        model = PrimitiveResultZneMetadataModel.model_validate(data)
        assert model.noise_factors is None

    def test_noise_factors_empty_list(self):
        """Test that noise_factors accepts empty list."""
        data = {"noise_factors": []}
        model = PrimitiveResultZneMetadataModel.model_validate(data)
        assert model.noise_factors == []

    def test_extrapolator_linear(self):
        """Test that extrapolator 'linear' is accepted."""
        data = {"noise_factors": [1.0], "extrapolator": "linear"}
        model = PrimitiveResultZneMetadataModel.model_validate(data)
        assert model.extrapolator == "linear"

    def test_extrapolator_exponential(self):
        """Test that extrapolator 'exponential' is accepted."""
        data = {"noise_factors": [1.0], "extrapolator": "exponential"}
        model = PrimitiveResultZneMetadataModel.model_validate(data)
        assert model.extrapolator == "exponential"

    def test_extrapolator_double_exponential(self):
        """Test that extrapolator 'double_exponential' is accepted."""
        data = {"noise_factors": [1.0], "extrapolator": "double_exponential"}
        model = PrimitiveResultZneMetadataModel.model_validate(data)
        assert model.extrapolator == "double_exponential"

    def test_extrapolator_polynomial_degree_1(self):
        """Test that extrapolator 'polynomial_degree_1' is accepted."""
        data = {"noise_factors": [1.0], "extrapolator": "polynomial_degree_1"}
        model = PrimitiveResultZneMetadataModel.model_validate(data)
        assert model.extrapolator == "polynomial_degree_1"

    def test_extrapolator_polynomial_degree_7(self):
        """Test that extrapolator 'polynomial_degree_7' is accepted."""
        data = {"noise_factors": [1.0], "extrapolator": "polynomial_degree_7"}
        model = PrimitiveResultZneMetadataModel.model_validate(data)
        assert model.extrapolator == "polynomial_degree_7"

    def test_extrapolator_fallback(self):
        """Test that extrapolator 'fallback' is accepted."""
        data = {"noise_factors": [1.0], "extrapolator": "fallback"}
        model = PrimitiveResultZneMetadataModel.model_validate(data)
        assert model.extrapolator == "fallback"

    def test_extrapolator_list(self):
        """Test that extrapolator accepts a list of extrapolators."""
        data = {
            "noise_factors": [1.0],
            "extrapolator": ["exponential", "linear", "fallback"],
        }
        model = PrimitiveResultZneMetadataModel.model_validate(data)
        assert model.extrapolator == ["exponential", "linear", "fallback"]

    def test_extrapolator_none(self):
        """Test that extrapolator can be None."""
        data = {"noise_factors": [1.0], "extrapolator": None}
        model = PrimitiveResultZneMetadataModel.model_validate(data)
        assert model.extrapolator is None

    def test_invalid_extrapolator(self):
        """Test that invalid extrapolator is rejected."""
        data = {"noise_factors": [1.0], "extrapolator": "invalid"}
        with pytest.raises(ValidationError):
            PrimitiveResultZneMetadataModel.model_validate(data)

    def test_extrapolated_noise_factors_list(self):
        """Test that extrapolated_noise_factors accepts a list."""
        data = {
            "noise_factors": [1.0],
            "extrapolated_noise_factors": [0.0, 0.5, 1.0, 1.5],
        }
        model = PrimitiveResultZneMetadataModel.model_validate(data)
        assert model.extrapolated_noise_factors == [0.0, 0.5, 1.0, 1.5]

    def test_extrapolated_noise_factors_empty_list(self):
        """Test that extrapolated_noise_factors accepts empty list."""
        data = {"noise_factors": [1.0], "extrapolated_noise_factors": []}
        model = PrimitiveResultZneMetadataModel.model_validate(data)
        assert model.extrapolated_noise_factors == []

    def test_extrapolated_noise_factors_none(self):
        """Test that extrapolated_noise_factors can be None."""
        data = {"noise_factors": [1.0], "extrapolated_noise_factors": None}
        model = PrimitiveResultZneMetadataModel.model_validate(data)
        assert model.extrapolated_noise_factors is None

    def test_all_polynomial_degrees(self):
        """Test that all polynomial degree extrapolators are accepted."""
        for degree in range(1, 8):
            data = {
                "noise_factors": [1.0],
                "extrapolator": f"polynomial_degree_{degree}",
            }
            model = PrimitiveResultZneMetadataModel.model_validate(data)
            assert model.extrapolator == f"polynomial_degree_{degree}"

    def test_mixed_extrapolator_list(self):
        """Test that a mixed list of extrapolators is accepted."""
        data = {
            "noise_factors": [1.0, 2.0],
            "extrapolator": [
                "linear",
                "exponential",
                "double_exponential",
                "polynomial_degree_3",
                "fallback",
            ],
        }
        model = PrimitiveResultZneMetadataModel.model_validate(data)
        assert len(model.extrapolator) == 5

    def test_serialization(self):
        """Test that serialization works correctly."""
        data = {
            "noise_factors": [1.0, 2.0, 3.0],
            "extrapolator": ["exponential", "linear"],
            "extrapolated_noise_factors": [0.0, 1.0, 2.0],
        }
        model = PrimitiveResultZneMetadataModel.model_validate(data)
        serialized = model.model_dump()
        assert serialized["noise_factors"] == [1.0, 2.0, 3.0]
        assert serialized["extrapolator"] == ["exponential", "linear"]
        assert serialized["extrapolated_noise_factors"] == [0.0, 1.0, 2.0]
