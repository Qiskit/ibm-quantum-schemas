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

"""Validation tests for dynamical_decoupling_metadata_model.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.models.estimator.version_0_1_dev.output.dynamical_decoupling_metadata_model import (
    DynamicalDecouplingMetadataModel,
)


class TestDynamicalDecouplingMetadataModelValidation:
    """Test DynamicalDecouplingMetadataModel validation."""

    def test_valid_metadata_with_defaults(self):
        """Test that metadata with default values is accepted."""
        model = DynamicalDecouplingMetadataModel.model_validate({})
        assert model.enable is False
        assert model.sequence_type == "XX"
        assert model.extra_slack_distribution == "middle"
        assert model.scheduling_method == "alap"

    def test_valid_metadata_with_custom_values(self):
        """Test that custom metadata values are accepted."""
        data = {
            "enable": True,
            "sequence_type": "XY4",
            "extra_slack_distribution": "edges",
            "scheduling_method": "asap",
        }
        model = DynamicalDecouplingMetadataModel.model_validate(data)
        assert model.enable is True
        assert model.sequence_type == "XY4"
        assert model.extra_slack_distribution == "edges"
        assert model.scheduling_method == "asap"

    def test_enable_true(self):
        """Test that enable can be set to True."""
        data = {"enable": True}
        model = DynamicalDecouplingMetadataModel.model_validate(data)
        assert model.enable is True

    def test_enable_false(self):
        """Test that enable can be set to False."""
        data = {"enable": False}
        model = DynamicalDecouplingMetadataModel.model_validate(data)
        assert model.enable is False

    def test_sequence_type_xx(self):
        """Test that sequence_type XX is accepted."""
        data = {"sequence_type": "XX"}
        model = DynamicalDecouplingMetadataModel.model_validate(data)
        assert model.sequence_type == "XX"

    def test_sequence_type_xpxm(self):
        """Test that sequence_type XpXm is accepted."""
        data = {"sequence_type": "XpXm"}
        model = DynamicalDecouplingMetadataModel.model_validate(data)
        assert model.sequence_type == "XpXm"

    def test_sequence_type_xy4(self):
        """Test that sequence_type XY4 is accepted."""
        data = {"sequence_type": "XY4"}
        model = DynamicalDecouplingMetadataModel.model_validate(data)
        assert model.sequence_type == "XY4"

    def test_invalid_sequence_type(self):
        """Test that invalid sequence_type is rejected."""
        data = {"sequence_type": "invalid"}
        with pytest.raises(ValidationError, match="Input should be 'XX', 'XpXm' or 'XY4'"):
            DynamicalDecouplingMetadataModel.model_validate(data)

    def test_extra_slack_distribution_middle(self):
        """Test that extra_slack_distribution middle is accepted."""
        data = {"extra_slack_distribution": "middle"}
        model = DynamicalDecouplingMetadataModel.model_validate(data)
        assert model.extra_slack_distribution == "middle"

    def test_extra_slack_distribution_edges(self):
        """Test that extra_slack_distribution edges is accepted."""
        data = {"extra_slack_distribution": "edges"}
        model = DynamicalDecouplingMetadataModel.model_validate(data)
        assert model.extra_slack_distribution == "edges"

    def test_invalid_extra_slack_distribution(self):
        """Test that invalid extra_slack_distribution is rejected."""
        data = {"extra_slack_distribution": "invalid"}
        with pytest.raises(ValidationError, match="Input should be 'middle' or 'edges'"):
            DynamicalDecouplingMetadataModel.model_validate(data)

    def test_scheduling_method_alap(self):
        """Test that scheduling_method alap is accepted."""
        data = {"scheduling_method": "alap"}
        model = DynamicalDecouplingMetadataModel.model_validate(data)
        assert model.scheduling_method == "alap"

    def test_scheduling_method_asap(self):
        """Test that scheduling_method asap is accepted."""
        data = {"scheduling_method": "asap"}
        model = DynamicalDecouplingMetadataModel.model_validate(data)
        assert model.scheduling_method == "asap"

    def test_invalid_scheduling_method(self):
        """Test that invalid scheduling_method is rejected."""
        data = {"scheduling_method": "invalid"}
        with pytest.raises(ValidationError, match="Input should be 'alap' or 'asap'"):
            DynamicalDecouplingMetadataModel.model_validate(data)

    def test_all_fields_together(self):
        """Test that all fields can be set together."""
        data = {
            "enable": True,
            "sequence_type": "XpXm",
            "extra_slack_distribution": "edges",
            "scheduling_method": "asap",
        }
        model = DynamicalDecouplingMetadataModel.model_validate(data)
        assert model.enable is True
        assert model.sequence_type == "XpXm"
        assert model.extra_slack_distribution == "edges"
        assert model.scheduling_method == "asap"

    def test_extra_fields_forbidden(self):
        """Test that extra fields are forbidden."""
        data = {"extra_field": "not allowed"}
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            DynamicalDecouplingMetadataModel.model_validate(data)

    def test_serialization(self):
        """Test that serialization works correctly."""
        data = {
            "enable": True,
            "sequence_type": "XY4",
            "extra_slack_distribution": "edges",
            "scheduling_method": "asap",
        }
        model = DynamicalDecouplingMetadataModel.model_validate(data)
        serialized = model.model_dump()
        assert serialized["enable"] is True
        assert serialized["sequence_type"] == "XY4"
        assert serialized["extra_slack_distribution"] == "edges"
        assert serialized["scheduling_method"] == "asap"

# Made with Bob
