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

"""Validation tests for pec_metadata_model.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.estimator.version_0_1_dev.pec_metadata import (
    PecMetadataModel,
)


class TestPecMetadataModelValidation:
    """Test PecMetadataModel validation."""

    def test_valid_empty_metadata(self):
        """Test that empty metadata is valid."""
        model = PecMetadataModel.model_validate({})
        assert model.num_randomizations_scaling is None

    def test_valid_with_num_randomizations_scaling(self):
        """Test that metadata with num_randomizations_scaling is valid."""
        data = {"num_randomizations_scaling": 1.5}
        model = PecMetadataModel.model_validate(data)
        assert model.num_randomizations_scaling == 1.5

    def test_num_randomizations_scaling_zero(self):
        """Test that num_randomizations_scaling can be zero."""
        data = {"num_randomizations_scaling": 0.0}
        model = PecMetadataModel.model_validate(data)
        assert model.num_randomizations_scaling == 0.0

    def test_num_randomizations_scaling_positive(self):
        """Test that num_randomizations_scaling accepts positive values."""
        data = {"num_randomizations_scaling": 2.5}
        model = PecMetadataModel.model_validate(data)
        assert model.num_randomizations_scaling == 2.5

    def test_num_randomizations_scaling_negative(self):
        """Test that num_randomizations_scaling accepts negative values."""
        data = {"num_randomizations_scaling": -1.0}
        model = PecMetadataModel.model_validate(data)
        assert model.num_randomizations_scaling == -1.0

    def test_num_randomizations_scaling_integer(self):
        """Test that num_randomizations_scaling accepts integers."""
        data = {"num_randomizations_scaling": 3}
        model = PecMetadataModel.model_validate(data)
        assert model.num_randomizations_scaling == 3.0

    def test_num_randomizations_scaling_none(self):
        """Test that num_randomizations_scaling can be None."""
        data = {"num_randomizations_scaling": None}
        model = PecMetadataModel.model_validate(data)
        assert model.num_randomizations_scaling is None

    def test_invalid_num_randomizations_scaling_string(self):
        """Test that string values are rejected for num_randomizations_scaling."""
        data = {"num_randomizations_scaling": "invalid"}
        with pytest.raises(ValidationError, match="Input should be a valid number"):
            PecMetadataModel.model_validate(data)

    def test_serialization(self):
        """Test that serialization works correctly."""
        data = {"num_randomizations_scaling": 1.5}
        model = PecMetadataModel.model_validate(data)
        serialized = model.model_dump()
        assert serialized["num_randomizations_scaling"] == 1.5

    def test_serialization_with_none(self):
        """Test that serialization works with None value."""
        model = PecMetadataModel.model_validate({})
        serialized = model.model_dump()
        assert serialized["num_randomizations_scaling"] is None
