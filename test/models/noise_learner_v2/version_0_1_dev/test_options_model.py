# This code is a Qiskit project.
#
# (C) Copyright IBM 2025.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Validation tests for options_model.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.models.noise_learner_v2.version_0_1_dev.options_model import (
    OptionsModel,
    SimulatorOptionsModel,
)


class TestSimulatorOptionsValidation:
    """Test SimulatorOptionsModel validation."""

    def test_valid_simulator_options(self):
        """Test that valid simulator options are accepted."""
        valid_options = {
            "seed_simulator": 42,
            "coupling_map": [[0, 1], [1, 2], [2, 3]],
            "basis_gates": ["u1", "u2", "u3", "cx"],
            "noise_model": None,
        }
        model = SimulatorOptionsModel.model_validate(valid_options)
        assert model.seed_simulator == 42
        assert model.coupling_map == [[0, 1], [1, 2], [2, 3]]
        assert model.basis_gates == ["u1", "u2", "u3", "cx"]
        assert model.noise_model is None

    def test_coupling_map_with_invalid_length(self):
        """Test that coupling_map entries with wrong length are rejected."""
        # Single element (should be 2)
        invalid_single = {"coupling_map": [[0]]}
        with pytest.raises(ValidationError):
            SimulatorOptionsModel.model_validate(invalid_single)

        # Three elements (should be 2)
        invalid_triple = {"coupling_map": [[0, 1, 2]]}
        with pytest.raises(ValidationError):
            SimulatorOptionsModel.model_validate(invalid_triple)

    def test_coupling_map_with_non_integers(self):
        """Test that coupling_map with non-integer values is rejected."""
        invalid = {"coupling_map": [["a", "b"]]}
        with pytest.raises(ValidationError):
            SimulatorOptionsModel.model_validate(invalid)

    def test_empty_coupling_map(self):
        """Test that empty coupling_map is accepted."""
        valid = {"coupling_map": []}
        model = SimulatorOptionsModel.model_validate(valid)
        assert model.coupling_map == []

    def test_all_none_values(self):
        """Test that all None values are accepted (defaults)."""
        model = SimulatorOptionsModel.model_validate({})
        assert model.seed_simulator is None
        assert model.coupling_map is None
        assert model.basis_gates is None
        assert model.noise_model is None


class TestOptionsModelValidation:
    """Test OptionsModel validation."""

    def test_valid_options_with_defaults(self):
        """Test that options with default values are accepted."""
        model = OptionsModel.model_validate({})
        assert model.max_layers_to_learn == 4
        assert model.shots_per_randomization == 128
        assert model.num_randomizations == 32
        assert model.layer_pair_depths == [0, 1, 2, 4, 16, 32]
        assert model.twirling_strategy == "active-accum"
        assert model.support_qiskit is True
        assert model.experimental is None
        assert model.simulator is None

    def test_valid_options_with_custom_values(self):
        """Test that custom option values are accepted."""
        options = {
            "max_layers_to_learn": 10,
            "shots_per_randomization": 256,
            "num_randomizations": 64,
            "layer_pair_depths": [0, 2, 8],
            "twirling_strategy": "active",
            "support_qiskit": False,
            "experimental": {"test": True},
            "simulator": {"seed_simulator": 123},
        }
        model = OptionsModel.model_validate(options)
        assert model.max_layers_to_learn == 10
        assert model.shots_per_randomization == 256
        assert model.num_randomizations == 64
        assert model.layer_pair_depths == [0, 2, 8]
        assert model.twirling_strategy == "active"
        assert model.support_qiskit is False
        assert model.experimental == {"test": True}
        assert isinstance(model.simulator, SimulatorOptionsModel)
        assert model.simulator.seed_simulator == 123

    def test_invalid_twirling_strategy(self):
        """Test that invalid twirling strategy is rejected."""
        options = {"twirling_strategy": "invalid-strategy"}
        with pytest.raises(ValidationError, match="Input should be 'active'"):
            OptionsModel.model_validate(options)

    def test_negative_shots_per_randomization(self):
        """Test that negative shots_per_randomization uses default."""
        # Pydantic doesn't validate this by default, just tests the model accepts it
        options = {"shots_per_randomization": -1}
        model = OptionsModel.model_validate(options)
        assert model.shots_per_randomization == -1  # No constraint defined

    def test_none_max_layers_to_learn(self):
        """Test that None is accepted for max_layers_to_learn."""
        options = {"max_layers_to_learn": None}
        model = OptionsModel.model_validate(options)
        assert model.max_layers_to_learn is None
