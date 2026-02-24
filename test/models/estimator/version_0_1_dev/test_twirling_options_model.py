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

"""Validation tests for twirling_options_model.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.models.estimator.version_0_1_dev.twirling_options_model import (
    TwirlingOptionsModel,
)


class TestTwirlingOptionsModelValidation:
    """Test TwirlingOptionsModel validation."""

    def test_valid_options_with_defaults(self):
        """Test that twirling options with default values are accepted."""
        model = TwirlingOptionsModel.model_validate({})
        
        # Verify all default values
        assert model.enable_gates is False
        assert model.enable_measure is True
        assert model.num_randomizations == "auto"
        assert model.shots_per_randomization == "auto"
        assert model.strategy == "active-accum"

    def test_valid_options_with_custom_values(self):
        """Test that custom twirling option values are accepted."""
        options = {
            "enable_gates": True,
            "enable_measure": False,
            "num_randomizations": 64,
            "shots_per_randomization": 128,
            "strategy": "active",
        }
        model = TwirlingOptionsModel.model_validate(options)
        assert model.enable_gates is True
        assert model.enable_measure is False
        assert model.num_randomizations == 64
        assert model.shots_per_randomization == 128
        assert model.strategy == "active"

    def test_enable_gates_true(self):
        """Test that enable_gates can be set to True."""
        options = {"enable_gates": True}
        model = TwirlingOptionsModel.model_validate(options)
        assert model.enable_gates is True

    def test_enable_gates_false(self):
        """Test that enable_gates can be set to False."""
        options = {"enable_gates": False}
        model = TwirlingOptionsModel.model_validate(options)
        assert model.enable_gates is False

    def test_enable_measure_true(self):
        """Test that enable_measure can be set to True."""
        options = {"enable_measure": True}
        model = TwirlingOptionsModel.model_validate(options)
        assert model.enable_measure is True

    def test_enable_measure_false(self):
        """Test that enable_measure can be set to False."""
        options = {"enable_measure": False}
        model = TwirlingOptionsModel.model_validate(options)
        assert model.enable_measure is False

    def test_num_randomizations_auto(self):
        """Test that num_randomizations can be 'auto'."""
        options = {"num_randomizations": "auto"}
        model = TwirlingOptionsModel.model_validate(options)
        assert model.num_randomizations == "auto"

    def test_num_randomizations_positive_integer(self):
        """Test that positive integer num_randomizations is accepted."""
        options = {"num_randomizations": 32}
        model = TwirlingOptionsModel.model_validate(options)
        assert model.num_randomizations == 32

    def test_num_randomizations_one(self):
        """Test that num_randomizations of 1 is accepted."""
        options = {"num_randomizations": 1}
        model = TwirlingOptionsModel.model_validate(options)
        assert model.num_randomizations == 1

    def test_num_randomizations_zero_rejected(self):
        """Test that num_randomizations of 0 is rejected."""
        options = {"num_randomizations": 0}
        with pytest.raises(ValidationError, match="greater than or equal to 1"):
            TwirlingOptionsModel.model_validate(options)

    def test_num_randomizations_negative_rejected(self):
        """Test that negative num_randomizations is rejected."""
        options = {"num_randomizations": -1}
        with pytest.raises(ValidationError, match="greater than or equal to 1"):
            TwirlingOptionsModel.model_validate(options)

    def test_shots_per_randomization_auto(self):
        """Test that shots_per_randomization can be 'auto'."""
        options = {"shots_per_randomization": "auto"}
        model = TwirlingOptionsModel.model_validate(options)
        assert model.shots_per_randomization == "auto"

    def test_shots_per_randomization_positive_integer(self):
        """Test that positive integer shots_per_randomization is accepted."""
        options = {"shots_per_randomization": 256}
        model = TwirlingOptionsModel.model_validate(options)
        assert model.shots_per_randomization == 256

    def test_shots_per_randomization_one(self):
        """Test that shots_per_randomization of 1 is accepted."""
        options = {"shots_per_randomization": 1}
        model = TwirlingOptionsModel.model_validate(options)
        assert model.shots_per_randomization == 1

    def test_shots_per_randomization_zero_rejected(self):
        """Test that shots_per_randomization of 0 is rejected."""
        options = {"shots_per_randomization": 0}
        with pytest.raises(ValidationError, match="greater than or equal to 1"):
            TwirlingOptionsModel.model_validate(options)

    def test_shots_per_randomization_negative_rejected(self):
        """Test that negative shots_per_randomization is rejected."""
        options = {"shots_per_randomization": -1}
        with pytest.raises(ValidationError, match="greater than or equal to 1"):
            TwirlingOptionsModel.model_validate(options)

    def test_strategy_active(self):
        """Test that strategy 'active' is accepted."""
        options = {"strategy": "active"}
        model = TwirlingOptionsModel.model_validate(options)
        assert model.strategy == "active"

    def test_strategy_active_accum(self):
        """Test that strategy 'active-accum' is accepted."""
        options = {"strategy": "active-accum"}
        model = TwirlingOptionsModel.model_validate(options)
        assert model.strategy == "active-accum"

    def test_strategy_active_circuit(self):
        """Test that strategy 'active-circuit' is accepted."""
        options = {"strategy": "active-circuit"}
        model = TwirlingOptionsModel.model_validate(options)
        assert model.strategy == "active-circuit"

    def test_strategy_all(self):
        """Test that strategy 'all' is accepted."""
        options = {"strategy": "all"}
        model = TwirlingOptionsModel.model_validate(options)
        assert model.strategy == "all"

    def test_invalid_strategy(self):
        """Test that invalid strategy is rejected."""
        options = {"strategy": "invalid"}
        with pytest.raises(
            ValidationError,
            match="Input should be 'active', 'active-accum', 'active-circuit' or 'all'",
        ):
            TwirlingOptionsModel.model_validate(options)

    def test_extra_fields_forbidden(self):
        """Test that extra fields are forbidden."""
        options = {"extra_field": "not allowed"}
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            TwirlingOptionsModel.model_validate(options)

    def test_all_options_together(self):
        """Test that all options can be set together."""
        options = {
            "enable_gates": True,
            "enable_measure": True,
            "num_randomizations": 48,
            "shots_per_randomization": 200,
            "strategy": "active-circuit",
        }
        model = TwirlingOptionsModel.model_validate(options)
        assert model.enable_gates is True
        assert model.enable_measure is True
        assert model.num_randomizations == 48
        assert model.shots_per_randomization == 200
        assert model.strategy == "active-circuit"

    def test_both_auto_values(self):
        """Test that both num_randomizations and shots_per_randomization can be 'auto'."""
        options = {
            "num_randomizations": "auto",
            "shots_per_randomization": "auto",
        }
        model = TwirlingOptionsModel.model_validate(options)
        assert model.num_randomizations == "auto"
        assert model.shots_per_randomization == "auto"


# Made with Bob