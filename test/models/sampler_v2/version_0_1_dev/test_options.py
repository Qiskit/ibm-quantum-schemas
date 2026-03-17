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

from ibm_quantum_schemas.sampler_v2.version_0_1_dev.options import OptionsModel


class TestOptionsModelValidation:
    """Test OptionsModel validation."""

    def test_valid_options_with_defaults(self):
        """Test that options with default values are accepted."""
        model = OptionsModel.model_validate({})
        assert model.default_shots == 4096
        assert model.dynamical_decoupling.enable is False
        assert model.execution.init_qubits is True
        assert model.twirling.strategy == "active-accum"
        assert model.simulator is None
        assert model.experimental == {}

    def test_valid_options_with_custom_values(self):
        """Test that custom option values are accepted."""
        options = {
            "default_shots": 1000,
            "dynamical_decoupling": {"enable": True, "sequence_type": "XY4"},
            "execution": {"init_qubits": False, "meas_type": "kerneled"},
            "twirling": {"enable_gates": True, "num_randomizations": 32},
            "simulator": {"seed_simulator": 123},
            "experimental": {"test": True},
        }
        model = OptionsModel.model_validate(options)
        assert model.default_shots == 1000
        assert model.dynamical_decoupling.enable is True
        assert model.dynamical_decoupling.sequence_type == "XY4"
        assert model.execution.init_qubits is False
        assert model.execution.meas_type == "kerneled"
        assert model.twirling.enable_gates is True
        assert model.twirling.num_randomizations == 32
        assert model.simulator.seed_simulator == 123
        assert model.experimental == {"test": True}
