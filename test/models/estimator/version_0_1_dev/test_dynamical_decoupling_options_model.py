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

"""Validation tests for dynamical_decoupling_options_model.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.models.estimator.version_0_1_dev import (
    dynamical_decoupling_options_model as dd_options,
)

DynamicalDecouplingOptionsModel = dd_options.DynamicalDecouplingOptionsModel


class TestDynamicalDecouplingOptionsModelValidation:
    """Test DynamicalDecouplingOptionsModel validation."""

    def test_valid_options_with_defaults(self):
        """Test that dynamical decoupling options with default values are accepted."""
        model = DynamicalDecouplingOptionsModel.model_validate({})

        # Verify all default values
        assert model.enable is False
        assert model.sequence_type == "XX"
        assert model.extra_slack_distribution == "middle"
        assert model.scheduling_method == "alap"
        assert model.skip_reset_qubits is False

    def test_valid_options_with_custom_values(self):
        """Test that custom dynamical decoupling option values are accepted."""
        options = {
            "enable": True,
            "sequence_type": "XY4",
            "extra_slack_distribution": "edges",
            "scheduling_method": "asap",
            "skip_reset_qubits": True,
        }
        model = DynamicalDecouplingOptionsModel.model_validate(options)
        assert model.enable is True
        assert model.sequence_type == "XY4"
        assert model.extra_slack_distribution == "edges"
        assert model.scheduling_method == "asap"
        assert model.skip_reset_qubits is True

    def test_sequence_type_xx(self):
        """Test that sequence_type XX is accepted."""
        options = {"sequence_type": "XX"}
        model = DynamicalDecouplingOptionsModel.model_validate(options)
        assert model.sequence_type == "XX"

    def test_sequence_type_xpxm(self):
        """Test that sequence_type XpXm is accepted."""
        options = {"sequence_type": "XpXm"}
        model = DynamicalDecouplingOptionsModel.model_validate(options)
        assert model.sequence_type == "XpXm"

    def test_sequence_type_xy4(self):
        """Test that sequence_type XY4 is accepted."""
        options = {"sequence_type": "XY4"}
        model = DynamicalDecouplingOptionsModel.model_validate(options)
        assert model.sequence_type == "XY4"

    def test_invalid_sequence_type(self):
        """Test that invalid sequence_type is rejected."""
        options = {"sequence_type": "invalid"}
        with pytest.raises(ValidationError, match="Input should be 'XX', 'XpXm' or 'XY4'"):
            DynamicalDecouplingOptionsModel.model_validate(options)

    def test_extra_slack_distribution_middle(self):
        """Test that extra_slack_distribution middle is accepted."""
        options = {"extra_slack_distribution": "middle"}
        model = DynamicalDecouplingOptionsModel.model_validate(options)
        assert model.extra_slack_distribution == "middle"

    def test_extra_slack_distribution_edges(self):
        """Test that extra_slack_distribution edges is accepted."""
        options = {"extra_slack_distribution": "edges"}
        model = DynamicalDecouplingOptionsModel.model_validate(options)
        assert model.extra_slack_distribution == "edges"

    def test_invalid_extra_slack_distribution(self):
        """Test that invalid extra_slack_distribution is rejected."""
        options = {"extra_slack_distribution": "invalid"}
        with pytest.raises(ValidationError, match="Input should be 'middle' or 'edges'"):
            DynamicalDecouplingOptionsModel.model_validate(options)

    def test_scheduling_method_alap(self):
        """Test that scheduling_method alap is accepted."""
        options = {"scheduling_method": "alap"}
        model = DynamicalDecouplingOptionsModel.model_validate(options)
        assert model.scheduling_method == "alap"

    def test_scheduling_method_asap(self):
        """Test that scheduling_method asap is accepted."""
        options = {"scheduling_method": "asap"}
        model = DynamicalDecouplingOptionsModel.model_validate(options)
        assert model.scheduling_method == "asap"

    def test_invalid_scheduling_method(self):
        """Test that invalid scheduling_method is rejected."""
        options = {"scheduling_method": "invalid"}
        with pytest.raises(ValidationError, match="Input should be 'alap' or 'asap'"):
            DynamicalDecouplingOptionsModel.model_validate(options)

    def test_enable_true(self):
        """Test that enable can be set to True."""
        options = {"enable": True}
        model = DynamicalDecouplingOptionsModel.model_validate(options)
        assert model.enable is True

    def test_enable_false(self):
        """Test that enable can be set to False."""
        options = {"enable": False}
        model = DynamicalDecouplingOptionsModel.model_validate(options)
        assert model.enable is False

    def test_skip_reset_qubits_true(self):
        """Test that skip_reset_qubits can be set to True."""
        options = {"skip_reset_qubits": True}
        model = DynamicalDecouplingOptionsModel.model_validate(options)
        assert model.skip_reset_qubits is True

    def test_skip_reset_qubits_false(self):
        """Test that skip_reset_qubits can be set to False."""
        options = {"skip_reset_qubits": False}
        model = DynamicalDecouplingOptionsModel.model_validate(options)
        assert model.skip_reset_qubits is False

    def test_extra_fields_forbidden(self):
        """Test that extra fields are forbidden."""
        options = {"extra_field": "not allowed"}
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            DynamicalDecouplingOptionsModel.model_validate(options)

    def test_all_options_together(self):
        """Test that all options can be set together."""
        options = {
            "enable": True,
            "sequence_type": "XpXm",
            "extra_slack_distribution": "edges",
            "scheduling_method": "asap",
            "skip_reset_qubits": True,
        }
        model = DynamicalDecouplingOptionsModel.model_validate(options)
        assert model.enable is True
        assert model.sequence_type == "XpXm"
        assert model.extra_slack_distribution == "edges"
        assert model.scheduling_method == "asap"
        assert model.skip_reset_qubits is True
