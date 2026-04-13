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

"""Validation tests for pub_result_zne_metadata_model.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.estimator.version_0_1.pub_result_zne_metadata import (  # noqa: E501
    PubResultZneMetadataModel,
)


class TestPubResultZneMetadataModelValidation:
    """Test PubResultZneMetadataModel validation."""

    def test_valid_empty_metadata(self):
        """Test that empty metadata is valid."""
        model = PubResultZneMetadataModel.model_validate({})
        assert model.extrapolator is None

    def test_valid_metadata_with_extrapolator_string(self):
        """Test that metadata with string extrapolator is valid."""
        data = {"extrapolator": "exponential"}
        model = PubResultZneMetadataModel.model_validate(data)
        assert model.extrapolator == "exponential"

    def test_valid_metadata_with_extrapolator_list(self):
        """Test that metadata with list extrapolator is valid."""
        data = {"extrapolator": ["exponential", "linear"]}
        model = PubResultZneMetadataModel.model_validate(data)
        assert model.extrapolator == ["exponential", "linear"]

    def test_extrapolator_linear(self):
        """Test that extrapolator 'linear' is accepted."""
        data = {"extrapolator": "linear"}
        model = PubResultZneMetadataModel.model_validate(data)
        assert model.extrapolator == "linear"

    def test_extrapolator_exponential(self):
        """Test that extrapolator 'exponential' is accepted."""
        data = {"extrapolator": "exponential"}
        model = PubResultZneMetadataModel.model_validate(data)
        assert model.extrapolator == "exponential"

    def test_extrapolator_double_exponential(self):
        """Test that extrapolator 'double_exponential' is accepted."""
        data = {"extrapolator": "double_exponential"}
        model = PubResultZneMetadataModel.model_validate(data)
        assert model.extrapolator == "double_exponential"

    def test_extrapolator_polynomial_degree_1(self):
        """Test that extrapolator 'polynomial_degree_1' is accepted."""
        data = {"extrapolator": "polynomial_degree_1"}
        model = PubResultZneMetadataModel.model_validate(data)
        assert model.extrapolator == "polynomial_degree_1"

    def test_extrapolator_polynomial_degree_2(self):
        """Test that extrapolator 'polynomial_degree_2' is accepted."""
        data = {"extrapolator": "polynomial_degree_2"}
        model = PubResultZneMetadataModel.model_validate(data)
        assert model.extrapolator == "polynomial_degree_2"

    def test_extrapolator_polynomial_degree_3(self):
        """Test that extrapolator 'polynomial_degree_3' is accepted."""
        data = {"extrapolator": "polynomial_degree_3"}
        model = PubResultZneMetadataModel.model_validate(data)
        assert model.extrapolator == "polynomial_degree_3"

    def test_extrapolator_polynomial_degree_4(self):
        """Test that extrapolator 'polynomial_degree_4' is accepted."""
        data = {"extrapolator": "polynomial_degree_4"}
        model = PubResultZneMetadataModel.model_validate(data)
        assert model.extrapolator == "polynomial_degree_4"

    def test_extrapolator_polynomial_degree_5(self):
        """Test that extrapolator 'polynomial_degree_5' is accepted."""
        data = {"extrapolator": "polynomial_degree_5"}
        model = PubResultZneMetadataModel.model_validate(data)
        assert model.extrapolator == "polynomial_degree_5"

    def test_extrapolator_polynomial_degree_6(self):
        """Test that extrapolator 'polynomial_degree_6' is accepted."""
        data = {"extrapolator": "polynomial_degree_6"}
        model = PubResultZneMetadataModel.model_validate(data)
        assert model.extrapolator == "polynomial_degree_6"

    def test_extrapolator_polynomial_degree_7(self):
        """Test that extrapolator 'polynomial_degree_7' is accepted."""
        data = {"extrapolator": "polynomial_degree_7"}
        model = PubResultZneMetadataModel.model_validate(data)
        assert model.extrapolator == "polynomial_degree_7"

    def test_extrapolator_fallback(self):
        """Test that extrapolator 'fallback' is accepted."""
        data = {"extrapolator": "fallback"}
        model = PubResultZneMetadataModel.model_validate(data)
        assert model.extrapolator == "fallback"

    def test_extrapolator_list_multiple(self):
        """Test that extrapolator accepts a list of multiple extrapolators."""
        data = {"extrapolator": ["exponential", "linear", "fallback"]}
        model = PubResultZneMetadataModel.model_validate(data)
        assert model.extrapolator == ["exponential", "linear", "fallback"]

    def test_extrapolator_list_single(self):
        """Test that extrapolator accepts a list with single extrapolator."""
        data = {"extrapolator": ["exponential"]}
        model = PubResultZneMetadataModel.model_validate(data)
        assert model.extrapolator == ["exponential"]

    def test_extrapolator_none(self):
        """Test that extrapolator can be None."""
        data = {"extrapolator": None}
        model = PubResultZneMetadataModel.model_validate(data)
        assert model.extrapolator is None

    def test_invalid_extrapolator_string(self):
        """Test that invalid extrapolator string is rejected."""
        data = {"extrapolator": "invalid"}
        with pytest.raises(ValidationError):
            PubResultZneMetadataModel.model_validate(data)

    def test_invalid_extrapolator_in_list(self):
        """Test that invalid extrapolator in list is rejected."""
        data = {"extrapolator": ["exponential", "invalid", "linear"]}
        with pytest.raises(ValidationError):
            PubResultZneMetadataModel.model_validate(data)

    def test_all_polynomial_degrees(self):
        """Test that all polynomial degree extrapolators are accepted."""
        for degree in range(1, 8):
            data = {"extrapolator": f"polynomial_degree_{degree}"}
            model = PubResultZneMetadataModel.model_validate(data)
            assert model.extrapolator == f"polynomial_degree_{degree}"

    def test_mixed_extrapolator_list(self):
        """Test that a mixed list of extrapolators is accepted."""
        data = {
            "extrapolator": [
                "linear",
                "exponential",
                "double_exponential",
                "polynomial_degree_3",
                "polynomial_degree_5",
                "fallback",
            ]
        }
        model = PubResultZneMetadataModel.model_validate(data)
        assert len(model.extrapolator) == 6

    def test_serialization_with_string(self):
        """Test that serialization works correctly with string extrapolator."""
        data = {"extrapolator": "exponential"}
        model = PubResultZneMetadataModel.model_validate(data)
        serialized = model.model_dump()
        assert serialized["extrapolator"] == "exponential"

    def test_serialization_with_list(self):
        """Test that serialization works correctly with list extrapolator."""
        data = {"extrapolator": ["exponential", "linear"]}
        model = PubResultZneMetadataModel.model_validate(data)
        serialized = model.model_dump()
        assert serialized["extrapolator"] == ["exponential", "linear"]

    def test_serialization_with_none(self):
        """Test that serialization works correctly with None extrapolator."""
        model = PubResultZneMetadataModel.model_validate({})
        serialized = model.model_dump()
        assert serialized["extrapolator"] is None
