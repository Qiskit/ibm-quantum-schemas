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
import zlib
from io import BytesIO

import numpy as np
import pybase64
from qiskit.circuit import QuantumCircuit

from ibm_quantum_schemas.models.estimator.version_0_1_dev.estimator_pub_model import (
    EstimatorPubModel,
)
from ibm_quantum_schemas.models.estimator.version_0_1_dev.models import OptionsModel


def _serialize_and_encode(array: np.ndarray) -> str:
    """Serialize and encode a numpy array to base64 string.
    
    Args:
        array: NumPy array to serialize
        
    Returns:
        Base64-encoded string of the compressed numpy array
    """
    buffer = BytesIO()
    np.save(buffer, array)
    array_data = buffer.getvalue()
    compressed = zlib.compress(array_data)
    encoded = pybase64.b64encode(compressed).decode("utf-8")
    return encoded


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



class TestEstimatorPubModelSerialization:
    """Test EstimatorPubModel serialization."""

    def test_estimator_pub_model_serialization(self, valid_typed_qpy_circuit_dict):
        """Test that EstimatorPubModel serialization."""
        str1 = '[{"__type__": "QuantumCircuit", "__value__": "eJwL9Az29gzhY2JmgALGgkIGrjQGDiCTiQEBQGxGmBIQkZxZlFyaWaJrZghTUl1byAhWychYyIAKGOEsNiTzsChidI5yTyxJBesvhIr9RwIwtQDDLRev"}, [{"YZ": 2.0, "XI": 1.0}, {"ZZ": 3.0, "XY": 4.0}], {"__type__": "ndarray", "__value__": "eJyb7BfqGxDJyFDGUK2eklqcXKRupaBuk2ahrqOgnpZfVFKUmBefX5SSChJ3S8wpTgWKF2ckFqQC+RoGOpo6CrUKFAAuAFOzG1s="}, 0.4]'

        obs1 = {"XI": 1, "YZ": 2}
        obs2 = {"ZZ": 3, "XY": 4}
        obs_array = [obs1, obs2]

        encoded_circ = valid_typed_qpy_circuit_dict
        encoded_args = {"__type__": "ndarray", "__value__": _serialize_and_encode(np.array([]))}
        
        pub_model = EstimatorPubModel.model_validate((encoded_circ, obs_array, encoded_args, 0.4))
        str2 = pub_model.model_dump_json(by_alias=True)

        dict1 = json.loads(str1)
        dict2 = json.loads(str2)

        print(dict1)
        print(dict2)

        assert dict1 == dict2
