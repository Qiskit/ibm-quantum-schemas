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

"""Validation tests for estimator models.py classes."""

import json

from ibm_quantum_schemas.models.estimator.version_0_1_dev.models import OptionsModel


class TestOptionsModelDefaults:
    """Test OptionsModel default values."""

    def test_options_model_default_serialization(self):
        """Test that OptionsModel with defaults serializes correctly."""
        options_model = OptionsModel()
        
        # Serialize to JSON string
        options_json = options_model.model_dump_json()
        
        # Parse back to dict
        options_dict = json.loads(options_json)
        
        # Expected default values
        expected = {
            'default_precision': 0.015625,
            'default_shots': None,
            'seed_estimator': None,
            'dynamical_decoupling': {
                'enable': False,
                'sequence_type': 'XX',
                'extra_slack_distribution': 'middle',
                'scheduling_method': 'alap',
                'skip_reset_qubits': False
            },
            'resilience': {
                'measure_mitigation': True,
                'measure_noise_learning': {
                    'num_randomizations': 32,
                    'shots_per_randomization': 'auto'
                },
                'zne_mitigation': False,
                'zne': {
                    'amplifier': 'gate_folding',
                    'noise_factors': [1.0, 3.0, 5.0],
                    'extrapolator': ['exponential', 'linear'],
                    'extrapolated_noise_factors': [0.0, 1.0, 3.0, 5.0]
                },
                'pec_mitigation': False,
                'pec': {
                    'max_overhead': 100.0,
                    'noise_gain': 'auto'
                },
                'layer_noise_learning': {
                    'max_layers_to_learn': 4,
                    'shots_per_randomization': 128,
                    'num_randomizations': 32,
                    'layer_pair_depths': [0, 1, 2, 4, 16, 32]
                },
                'layer_noise_model': None
            },
            'execution': {
                'init_qubits': True,
                'rep_delay': None
            },
            'twirling': {
                'enable_gates': False,
                'enable_measure': True,
                'num_randomizations': 'auto',
                'shots_per_randomization': 'auto',
                'strategy': 'active-accum'
            },
            'experimental': {}
        }
        
        assert options_dict == expected
