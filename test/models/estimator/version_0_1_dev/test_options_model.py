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

"""Validation tests for options_model.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.models.estimator.version_0_1_dev.options_model import OptionsModel


class TestOptionsModelValidation:
    """Test OptionsModel validation."""

    def test_valid_options_with_defaults(self):
        """Test that options with default values are accepted."""
        model = OptionsModel.model_validate({})
        assert model.default_precision == 0.015625
        assert model.default_shots is None
        assert model.seed_estimator is None
        
        # Verify dynamical_decoupling defaults
        assert model.dynamical_decoupling.enable is False
        assert model.dynamical_decoupling.sequence_type == "XX"
        assert model.dynamical_decoupling.extra_slack_distribution == "middle"
        assert model.dynamical_decoupling.scheduling_method == "alap"
        assert model.dynamical_decoupling.skip_reset_qubits is False
        
        # Verify resilience defaults
        assert model.resilience.measure_mitigation is True
        assert model.resilience.zne_mitigation is False
        assert model.resilience.pec_mitigation is False
        assert model.resilience.layer_noise_model is None
        
        # Verify execution defaults
        assert model.execution.init_qubits is True
        assert model.execution.rep_delay is None
        
        # Verify twirling defaults
        assert model.twirling.enable_gates is False
        assert model.twirling.enable_measure is True
        assert model.twirling.num_randomizations == "auto"
        assert model.twirling.shots_per_randomization == "auto"
        assert model.twirling.strategy == "active-accum"
        
        # Verify simulator defaults
        assert model.simulator.noise_model is None
        assert model.simulator.seed_simulator is None
        assert model.simulator.coupling_map is None
        assert model.simulator.basis_gates is None
        
        assert model.experimental == {}

    def test_valid_options_with_custom_values(self):
        """Test that custom option values are accepted."""
        options = {
            "default_precision": 0.01,
            "default_shots": 1000,
            "seed_estimator": 42,
            "experimental": {"test": True},
        }
        model = OptionsModel.model_validate(options)
        assert model.default_precision == 0.01
        assert model.default_shots == 1000
        assert model.seed_estimator == 42
        assert model.experimental == {"test": True}

    def test_negative_default_precision(self):
        """Test that negative default_precision is rejected."""
        options = {"default_precision": -0.01}
        with pytest.raises(ValidationError, match="greater than or equal to 0"):
            OptionsModel.model_validate(options)

    def test_zero_default_precision(self):
        """Test that zero default_precision is rejected."""
        options = {"default_precision": 0.0}
        with pytest.raises(ValidationError, match="greater than 0"):
            OptionsModel.model_validate(options)

    def test_negative_default_shots(self):
        """Test that negative default_shots is rejected."""
        options = {"default_shots": -1}
        with pytest.raises(ValidationError, match="greater than or equal to 1"):
            OptionsModel.model_validate(options)

    def test_zero_default_shots(self):
        """Test that zero default_shots is rejected."""
        options = {"default_shots": 0}
        with pytest.raises(ValidationError, match="greater than or equal to 1"):
            OptionsModel.model_validate(options)

    def test_one_default_shots(self):
        """Test that default_shots of 1 is accepted."""
        options = {"default_shots": 1}
        model = OptionsModel.model_validate(options)
        assert model.default_shots == 1

    def test_negative_seed_estimator(self):
        """Test that negative seed_estimator is rejected."""
        options = {"seed_estimator": -1}
        with pytest.raises(ValidationError, match="greater than or equal to 0"):
            OptionsModel.model_validate(options)

    def test_zero_seed_estimator(self):
        """Test that zero seed_estimator is accepted."""
        options = {"seed_estimator": 0}
        model = OptionsModel.model_validate(options)
        assert model.seed_estimator == 0

    def test_nested_dynamical_decoupling_options(self):
        """Test that nested dynamical_decoupling options are accepted."""
        options = {
            "dynamical_decoupling": {
                "enable": True,
                "sequence_type": "XY4",
            }
        }
        model = OptionsModel.model_validate(options)
        assert model.dynamical_decoupling.enable is True
        assert model.dynamical_decoupling.sequence_type == "XY4"

    def test_nested_resilience_options(self):
        """Test that nested resilience options are accepted."""
        options = {
            "resilience": {
                "measure_mitigation": True,
                "zne_mitigation": False,
                "pec_mitigation": False,
            }
        }
        model = OptionsModel.model_validate(options)
        assert model.resilience.measure_mitigation is True
        assert model.resilience.zne_mitigation is False
        assert model.resilience.pec_mitigation is False

    def test_nested_execution_options(self):
        """Test that nested execution options are accepted."""
        options = {
            "execution": {
                "init_qubits": True,
                "rep_delay": 0.0001,
            }
        }
        model = OptionsModel.model_validate(options)
        assert model.execution.init_qubits is True
        assert model.execution.rep_delay == 0.0001

    def test_nested_twirling_options(self):
        """Test that nested twirling options are accepted."""
        options = {
            "twirling": {
                "enable_gates": True,
                "enable_measure": True,
                "num_randomizations": 32,
            }
        }
        model = OptionsModel.model_validate(options)
        assert model.twirling.enable_gates is True
        assert model.twirling.enable_measure is True
        assert model.twirling.num_randomizations == 32

    def test_nested_simulator_options(self):
        """Test that nested simulator options are accepted."""
        options = {
            "simulator": {
                "seed_simulator": 123,
                "coupling_map": [[0, 1], [1, 2]],
            }
        }
        model = OptionsModel.model_validate(options)
        assert model.simulator.seed_simulator == 123
        assert model.simulator.coupling_map == [[0, 1], [1, 2]]

    def test_extra_fields_forbidden(self):
        """Test that extra fields are forbidden."""
        options = {"extra_field": "not allowed"}
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            OptionsModel.model_validate(options)

    def test_none_default_shots(self):
        """Test that None is accepted for default_shots."""
        options = {"default_shots": None}
        model = OptionsModel.model_validate(options)
        assert model.default_shots is None

    def test_none_seed_estimator(self):
        """Test that None is accepted for seed_estimator."""
        options = {"seed_estimator": None}
        model = OptionsModel.model_validate(options)
        assert model.seed_estimator is None

