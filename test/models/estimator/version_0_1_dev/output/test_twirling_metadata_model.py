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

"""Validation tests for twirling_metadata_model.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.models.estimator.version_0_1_dev.output.twirling_metadata_model import (
    TwirlingMetadataModel,
)


class TestTwirlingMetadataModelValidation:
    """Test TwirlingMetadataModel validation."""

    def test_valid_metadata_with_defaults(self):
        """Test that metadata with default values is accepted."""
        model = TwirlingMetadataModel.model_validate({})
        assert model.enable_gates is None
        assert model.enable_measure is True
        assert model.num_randomizations == "auto"
        assert model.shots_per_randomization == "auto"
        assert model.strategy == "active-accum"
        assert model.interleave_randomizations is True

    def test_valid_metadata_with_custom_values(self):
        """Test that custom metadata values are accepted."""
        data = {
            "enable_gates": True,
            "enable_measure": False,
            "num_randomizations": 100,
            "shots_per_randomization": 64,
            "strategy": "all",
            "interleave_randomizations": False,
        }
        model = TwirlingMetadataModel.model_validate(data)
        assert model.enable_gates is True
        assert model.enable_measure is False
        assert model.num_randomizations == 100
        assert model.shots_per_randomization == 64
        assert model.strategy == "all"
        assert model.interleave_randomizations is False

    def test_enable_gates_true(self):
        """Test that enable_gates can be set to True."""
        data = {"enable_gates": True}
        model = TwirlingMetadataModel.model_validate(data)
        assert model.enable_gates is True

    def test_enable_gates_false(self):
        """Test that enable_gates can be set to False."""
        data = {"enable_gates": False}
        model = TwirlingMetadataModel.model_validate(data)
        assert model.enable_gates is False

    def test_enable_gates_none(self):
        """Test that enable_gates can be None."""
        data = {"enable_gates": None}
        model = TwirlingMetadataModel.model_validate(data)
        assert model.enable_gates is None

    def test_enable_measure_true(self):
        """Test that enable_measure can be set to True."""
        data = {"enable_measure": True}
        model = TwirlingMetadataModel.model_validate(data)
        assert model.enable_measure is True

    def test_enable_measure_false(self):
        """Test that enable_measure can be set to False."""
        data = {"enable_measure": False}
        model = TwirlingMetadataModel.model_validate(data)
        assert model.enable_measure is False

    def test_num_randomizations_auto(self):
        """Test that num_randomizations can be 'auto'."""
        data = {"num_randomizations": "auto"}
        model = TwirlingMetadataModel.model_validate(data)
        assert model.num_randomizations == "auto"

    def test_num_randomizations_positive_integer(self):
        """Test that num_randomizations accepts positive integers."""
        data = {"num_randomizations": 50}
        model = TwirlingMetadataModel.model_validate(data)
        assert model.num_randomizations == 50

    def test_num_randomizations_one(self):
        """Test that num_randomizations accepts 1."""
        data = {"num_randomizations": 1}
        model = TwirlingMetadataModel.model_validate(data)
        assert model.num_randomizations == 1

    def test_num_randomizations_zero_rejected(self):
        """Test that num_randomizations rejects 0."""
        data = {"num_randomizations": 0}
        with pytest.raises(ValidationError, match="greater than or equal to 1"):
            TwirlingMetadataModel.model_validate(data)

    def test_num_randomizations_negative_rejected(self):
        """Test that num_randomizations rejects negative values."""
        data = {"num_randomizations": -5}
        with pytest.raises(ValidationError, match="greater than or equal to 1"):
            TwirlingMetadataModel.model_validate(data)

    def test_shots_per_randomization_auto(self):
        """Test that shots_per_randomization can be 'auto'."""
        data = {"shots_per_randomization": "auto"}
        model = TwirlingMetadataModel.model_validate(data)
        assert model.shots_per_randomization == "auto"

    def test_shots_per_randomization_positive_integer(self):
        """Test that shots_per_randomization accepts positive integers."""
        data = {"shots_per_randomization": 128}
        model = TwirlingMetadataModel.model_validate(data)
        assert model.shots_per_randomization == 128

    def test_shots_per_randomization_one(self):
        """Test that shots_per_randomization accepts 1."""
        data = {"shots_per_randomization": 1}
        model = TwirlingMetadataModel.model_validate(data)
        assert model.shots_per_randomization == 1

    def test_shots_per_randomization_zero_rejected(self):
        """Test that shots_per_randomization rejects 0."""
        data = {"shots_per_randomization": 0}
        with pytest.raises(ValidationError, match="greater than or equal to 1"):
            TwirlingMetadataModel.model_validate(data)

    def test_shots_per_randomization_negative_rejected(self):
        """Test that shots_per_randomization rejects negative values."""
        data = {"shots_per_randomization": -10}
        with pytest.raises(ValidationError, match="greater than or equal to 1"):
            TwirlingMetadataModel.model_validate(data)

    def test_strategy_active(self):
        """Test that strategy 'active' is accepted."""
        data = {"strategy": "active"}
        model = TwirlingMetadataModel.model_validate(data)
        assert model.strategy == "active"

    def test_strategy_active_accum(self):
        """Test that strategy 'active-accum' is accepted."""
        data = {"strategy": "active-accum"}
        model = TwirlingMetadataModel.model_validate(data)
        assert model.strategy == "active-accum"

    def test_strategy_active_circuit(self):
        """Test that strategy 'active-circuit' is accepted."""
        data = {"strategy": "active-circuit"}
        model = TwirlingMetadataModel.model_validate(data)
        assert model.strategy == "active-circuit"

    def test_strategy_all(self):
        """Test that strategy 'all' is accepted."""
        data = {"strategy": "all"}
        model = TwirlingMetadataModel.model_validate(data)
        assert model.strategy == "all"

    def test_invalid_strategy(self):
        """Test that invalid strategy is rejected."""
        data = {"strategy": "invalid"}
        with pytest.raises(
            ValidationError,
            match="Input should be 'active', 'active-accum', 'active-circuit' or 'all'",
        ):
            TwirlingMetadataModel.model_validate(data)

    def test_interleave_randomizations_true(self):
        """Test that interleave_randomizations can be True."""
        data = {"interleave_randomizations": True}
        model = TwirlingMetadataModel.model_validate(data)
        assert model.interleave_randomizations is True

    def test_interleave_randomizations_false(self):
        """Test that interleave_randomizations can be False."""
        data = {"interleave_randomizations": False}
        model = TwirlingMetadataModel.model_validate(data)
        assert model.interleave_randomizations is False

    def test_all_fields_together(self):
        """Test that all fields can be set together."""
        data = {
            "enable_gates": True,
            "enable_measure": False,
            "num_randomizations": 200,
            "shots_per_randomization": 32,
            "strategy": "active-circuit",
            "interleave_randomizations": False,
        }
        model = TwirlingMetadataModel.model_validate(data)
        assert model.enable_gates is True
        assert model.enable_measure is False
        assert model.num_randomizations == 200
        assert model.shots_per_randomization == 32
        assert model.strategy == "active-circuit"
        assert model.interleave_randomizations is False

    def test_extra_fields_forbidden(self):
        """Test that extra fields are forbidden."""
        data = {"extra_field": "not allowed"}
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            TwirlingMetadataModel.model_validate(data)

    def test_serialization(self):
        """Test that serialization works correctly."""
        data = {
            "enable_gates": True,
            "enable_measure": False,
            "num_randomizations": 100,
            "shots_per_randomization": 64,
            "strategy": "all",
            "interleave_randomizations": False,
        }
        model = TwirlingMetadataModel.model_validate(data)
        serialized = model.model_dump()
        assert serialized["enable_gates"] is True
        assert serialized["enable_measure"] is False
        assert serialized["num_randomizations"] == 100
        assert serialized["shots_per_randomization"] == 64
        assert serialized["strategy"] == "all"
        assert serialized["interleave_randomizations"] is False

# Made with Bob
