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

import numpy as np
from qiskit.circuit import Parameter, QuantumCircuit

from ibm_quantum_schemas.models.estimator.version_0_1_dev.estimator_pub_model import (
    EstimatorPubModel,
)
from ibm_quantum_schemas.models.estimator.version_0_1_dev.models import (
    OptionsModel,
    ParamsModel,
)

from ...utils import valid_typed_qpy_circuit_dict


class TestOptionsModel:
    """Test OptionsModel."""

    def test_options_model(self):
        """Test OptionsModel."""
        options_model = OptionsModel()
        options_dict = options_model.model_dump_json()

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


class TestEstimatorPubModel:
    """Test EstimatorPubModel."""

    def test_estimator_pub_model(self):
        """Test EstimatorPubModel."""
        str1 = '[{"__type__": "QuantumCircuit", "__value__": "eJwL9Az29gzhY2JmgALGgkIGrjQGDiCTiQEBQGxGmBIQkZxZlFyaWaJrYghTUl1byAhWychYyIAKGOEsNiTzsChidI5yTyxJBesvhIr9RwIwtQDCQRet"}, [{"YZ": 2.0, "XI": 1.0}, {"ZZ": 3.0, "XY": 4.0}], {"__type__": "ndarray", "__value__": "eJyb7BfqGxDJyFDGUK2eklqcXKRupaBuk2ahrqOgnpZfVFKUmBefX5SSChJ3S8wpTgWKF2ckFqQC+RoGOpo6CrUKFAAuAFOzG1s="}, null]'

        obs1 = {"XI": 1, "YZ": 2}
        obs2 = {"ZZ": 3, "XY": 4}
        obs_array = [obs1, obs2]

        circuit = QuantumCircuit(2)
        circuit.cz(0, 1)
        encoded_circ = valid_typed_qpy_circuit_dict(circuit)
        
        # Use defaults for parameter_values (empty array) and precision (None)
        pub_model = EstimatorPubModel.model_validate((encoded_circ, obs_array))
        str2 = pub_model.model_dump_json(by_alias=True)

        dict1 = json.loads(str1)
        dict2 = json.loads(str2)

        # qpy serializations of the same circuit are different
        del(dict1[0]["__value__"])
        del(dict2[0]["__value__"])

        assert dict1 == dict2


class TestParamsModel:
    """Test ParamsModel."""

    def test_params_model(self):
        """Test ParamsModel."""
        str1 = '{"pubs": [[{"__type__": "QuantumCircuit", "__value__": "eJwL9Az29gzhY2JmgALGgkIGrjQGDiCTiQEBQGxGmBIQkZxZlFyaWaJrZghTUl1byAhWychYyIAKGOEsNiTzsChidI5yTyxJBesvhIr9RwIwtQDDLRev"}, {"ZZ": 1.0}, {"__type__": "ndarray", "__value__": "eJyb7BfqGxDJyFDGUK2eklqcXKRupaBuk2ahrqOgnpZfVFKUmBefX5SSChJ3S8wpTgWKF2ckFqQC+RoGOpo6CrUKFAAuAFOzG1s="}, null], [{"__type__": "QuantumCircuit", "__value__": "eJwL9Az29gzhY2JmgALGgkIGrjQGDhCTAQGYkPhgOjmzKLk0s0TXzAimpLq2kBEsy8hYyIAO2KD6GDFkICAoyj2xJBWsrwAqJMzA2JLy829phvPZCZGn3OPENWaApP4jAZhuAKa3IDY="}, [{"Z": 1.0}], {"__type__": "ndarray", "__value__": "eJyb7BfqGxDJyFDGUK2eklqcXKRupaBuk2ahrqOgnpZfVFKUmBefX5SSChJ3S8wpTgWKF2ckFqQC+RqGOpo6CrUKFAAuBjDgcAAALzUbpA=="}, null]], "options": {"default_precision": 0.015625, "default_shots": null, "dynamical_decoupling": {"enable": false, "sequence_type": "XX", "extra_slack_distribution": "middle", "scheduling_method": "alap", "skip_reset_qubits": false}, "resilience": {"measure_mitigation": true, "measure_noise_learning": {"num_randomizations": 32, "shots_per_randomization": "auto"}, "zne_mitigation": false, "zne": {"amplifier": "gate_folding", "noise_factors": [1.0, 3.0, 5.0], "extrapolator": ["exponential", "linear"], "extrapolated_noise_factors": [0.0, 1.0, 3.0, 5.0]}, "pec_mitigation": false, "pec": {"max_overhead": 100.0, "noise_gain": "auto"}, "layer_noise_learning": {"max_layers_to_learn": 4, "shots_per_randomization": 128, "num_randomizations": 32, "layer_pair_depths": [0, 1, 2, 4, 16, 32]}, "layer_noise_model": null}, "twirling": {"enable_gates": false, "enable_measure": true, "num_randomizations": "auto", "shots_per_randomization": "auto", "strategy": "active-accum"}}, "version": 2, "support_qiskit": true}'

        circ = QuantumCircuit(2)
        circ.cz(0, 1)
        
        pcirc = QuantumCircuit(1)
        pcirc.rz(Parameter("p"), 0)
        
        encoded_circ1 = valid_typed_qpy_circuit_dict(circ)
        encoded_circ2 = valid_typed_qpy_circuit_dict(pcirc)
        
        pub1 = (encoded_circ1, "ZZ")
        pub2 = (encoded_circ2, ["Z"], np.array([3]))
        
        params_model = ParamsModel(
            pubs=[pub1, pub2],
            options=OptionsModel()
        )
        str2 = params_model.model_dump_json(by_alias=True)

        dict1 = json.loads(str1)
        dict2 = json.loads(str2)
        
        # qpy serializations of the same circuit are different
        del dict1["pubs"][0][0]["__value__"]
        del dict1["pubs"][1][0]["__value__"]
        del dict2["pubs"][0][0]["__value__"]
        del dict2["pubs"][1][0]["__value__"]
     
        assert dict1 == dict2
