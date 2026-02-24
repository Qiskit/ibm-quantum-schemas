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

"""Validation tests for execution_options_model.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.models.estimator.version_0_1_dev.execution_options_model import (
    ExecutionOptionsV2Model,
)


class TestExecutionOptionsV2ModelValidation:
    """Test ExecutionOptionsV2Model validation."""

    def test_valid_options_with_defaults(self):
        """Test that execution options with default values are accepted."""
        model = ExecutionOptionsV2Model.model_validate({})
        
        # Verify all default values
        assert model.init_qubits is True
        assert model.rep_delay is None

    def test_valid_options_with_custom_values(self):
        """Test that custom execution option values are accepted."""
        options = {
            "init_qubits": False,
            "rep_delay": 0.0001,
        }
        model = ExecutionOptionsV2Model.model_validate(options)
        assert model.init_qubits is False
        assert model.rep_delay == 0.0001

    def test_init_qubits_true(self):
        """Test that init_qubits can be set to True."""
        options = {"init_qubits": True}
        model = ExecutionOptionsV2Model.model_validate(options)
        assert model.init_qubits is True

    def test_init_qubits_false(self):
        """Test that init_qubits can be set to False."""
        options = {"init_qubits": False}
        model = ExecutionOptionsV2Model.model_validate(options)
        assert model.init_qubits is False

    def test_rep_delay_none(self):
        """Test that rep_delay can be None."""
        options = {"rep_delay": None}
        model = ExecutionOptionsV2Model.model_validate(options)
        assert model.rep_delay is None

    def test_rep_delay_zero(self):
        """Test that rep_delay can be zero."""
        options = {"rep_delay": 0.0}
        model = ExecutionOptionsV2Model.model_validate(options)
        assert model.rep_delay == 0.0

    def test_rep_delay_positive(self):
        """Test that positive rep_delay is accepted."""
        options = {"rep_delay": 0.0005}
        model = ExecutionOptionsV2Model.model_validate(options)
        assert model.rep_delay == 0.0005

    def test_rep_delay_negative_rejected(self):
        """Test that negative rep_delay is rejected."""
        options = {"rep_delay": -0.0001}
        with pytest.raises(ValidationError, match="greater than or equal to 0"):
            ExecutionOptionsV2Model.model_validate(options)

    def test_rep_delay_large_value(self):
        """Test that large rep_delay values are accepted."""
        options = {"rep_delay": 1.0}
        model = ExecutionOptionsV2Model.model_validate(options)
        assert model.rep_delay == 1.0

    def test_extra_fields_forbidden(self):
        """Test that extra fields are forbidden."""
        options = {"extra_field": "not allowed"}
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            ExecutionOptionsV2Model.model_validate(options)

    def test_all_options_together(self):
        """Test that all options can be set together."""
        options = {
            "init_qubits": False,
            "rep_delay": 0.00025,
        }
        model = ExecutionOptionsV2Model.model_validate(options)
        assert model.init_qubits is False
        assert model.rep_delay == 0.00025

    def test_invalid_init_qubits_type(self):
        """Test that invalid init_qubits type is rejected."""
        options = {"init_qubits": "true"}
        with pytest.raises(ValidationError, match="Input should be a valid boolean"):
            ExecutionOptionsV2Model.model_validate(options)

    def test_invalid_rep_delay_type(self):
        """Test that invalid rep_delay type is rejected."""
        options = {"rep_delay": "0.0001"}
        with pytest.raises(ValidationError, match="Input should be a valid number"):
            ExecutionOptionsV2Model.model_validate(options)


# Made with Bob