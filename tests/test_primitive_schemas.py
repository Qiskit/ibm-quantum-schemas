# This code is part of Qiskit.
#
# (C) Copyright IBM 2024
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

import json
import os
import unittest
import ddt
import jsonschema

from qiskit_ibm_runtime import EstimatorOptions, SamplerOptions
from tests import combine

SCHEMAS_PATH = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'schemas')

@ddt.ddt
class TestEstimatorV2Schema(unittest.TestCase):
    """Tests the estimator schema agrees with the format of the qiskit runtime estimator API calls"""
    def setUp(self) -> None:
        with open(os.path.join(SCHEMAS_PATH, 'estimator_v2_schema.json'), 'r') as fd:
            self.estimator_schema = json.load(fd)
        self.validator = jsonschema.Draft202012Validator(schema=self.estimator_schema)

    @staticmethod
    def get_converted_options(options_dict):
        """Emulate the process in `qiskit-ibm-runtime` where the EstimatorOptions
        are converted to a filtered options dictionary"""
        converted_options = EstimatorOptions._get_program_inputs(options_dict)
        if 'pubs' not in converted_options:
            converted_options['pubs'] = []
        return converted_options

    def assert_valid_options(self, options_dict):
        """Verifies the schema validation gives the same result as attempting
        to set the options in the estimator"""
        converted_options = self.get_converted_options(options_dict)
        error_message = None
        options_valid = True
        try:
            self.validator.validate(converted_options)
        except Exception as err:
            options_valid = False
            error_message = str(err)

        estimator_options_valid = True
        try:
            EstimatorOptions(**options_dict)
        except Exception as err:
            estimator_options_valid = False
            error_message = str(err)

        if estimator_options_valid:
            self.assertTrue(options_valid, msg=f"Options should pass the JSON schema validation, but it failed with the message:\n{error_message}")
        else:
            self.assertFalse(options_valid, msg=f"Options passed the JSON schema validation, but it should fail since for EstimatorOptions it fails with the message:\n{error_message}")

    @ddt.data(0, 1, 2, 3, -1, 17, 3.5)
    def test_resilience_level(self, level):
        """Testing various values of the resilience level"""
        options = {'resilience_level': level}
        self.assert_valid_options(options)

    @ddt.data(0, 1, 3.5)
    def test_seed_estimator(self, seed):
        """Testing various values of the seed estimator"""
        options = {'seed_estimator': seed}
        self.assert_valid_options(options)

    @ddt.data(0, 1, 3.5)
    def test_default_precision(self, precision):
        """Testing various values of the default precision"""
        options = {'default_precision': precision}
        self.assert_valid_options(options)

    @ddt.data(0, 1, 3.5, -2)
    def test_default_shots(self, shots):
        """Testing various values of the default shots"""
        options = {'default_shots': shots}
        self.assert_valid_options(options)

    @combine(enable=[True, False, 13],
             sequence_type=["XX", "XpXm", "XY4", "ZZ", 13],
             extra_slack_distribution=["middle", "edges", "end", 13],
             scheduling_method=["alap", "asap", "lapsap", 13]
             )
    def test_dynamical_decoupling(self, enable, sequence_type, extra_slack_distribution, scheduling_method):
        """Testing various values of dynamical decoupling"""
        options = {
            'dynamical_decoupling':{
                'enable': enable,
                'sequence_type': sequence_type,
                'extra_slack_distribution': extra_slack_distribution,
                'scheduling_method': scheduling_method
            }
        }
        self.assert_valid_options(options)

    @ddt.data(0, 1, 3.5, -2)
    def test_optimization_level(self, optimization_level):
        """Testing various values of the optimization level options"""
        options = {'optimization_level': optimization_level}
        self.assert_valid_options(options)

    @combine(num_randomizations=[0, 1, 2, "False"],
             shots_per_randomization=[0, 1, 2, "False", "auto"],
             enable_measure_mitigation=[True, False],
             )
    def test_measure_noise_learning(self, num_randomizations, shots_per_randomization, enable_measure_mitigation):
        """Testing various values of measure noise learning"""
        options = {
            'resilience': {
                'measure_noise_learning': {
                    'num_randomizations': num_randomizations,
                    'shots_per_randomization': shots_per_randomization,
                },
                'measure_mitigation': enable_measure_mitigation
            }
        }
        self.assert_valid_options(options)

    @combine(noise_factors=[[17], [1,2], [1,4,8], [1.3, 3.2], False],
             extrapolator=["linear", "exponential", "double_exponential",
                               "polynomial_degree_1", "polynomial_degree_2", "polynomial_degree_3",
                               "polynomial_degree_4", "polynomial_degree_5", "polynomial_degree_6",
                               "polynomial_degree_7", ["linear", "exponential", "polynomial_degree_3"], "false_extrapolator",
                               13, False, [13, "linear"]
                               ],
             enable_zne_mitigation=[True, False],
             )
    def test_zne_mitigation_options(self, noise_factors, extrapolator, enable_zne_mitigation):
        """Testing various values of pec mitigation"""
        options = {
            'resilience': {
                'zne': {
                    'noise_factors': noise_factors,
                    'extrapolator': extrapolator,
                },
                'zne_mitigation': enable_zne_mitigation
            }
        }
        self.assert_valid_options(options)

    @combine(max_layers_to_learn=[0, 1, 15, -3],
             shots_per_randomization=[0, 1, 15, -3],
             num_randomizations=[0, 1, 15, -3],
             layer_pair_depths=[[0, 1, 15], 15, [0, -3]]
             )
    def test_layer_noise_learning_options(self, max_layers_to_learn, shots_per_randomization, num_randomizations, layer_pair_depths):
        """Testing various values of layer noise learning"""
        options = {
            'resilience': {
                'layer_noise_learning': {
                    'max_layers_to_learn': max_layers_to_learn,
                    'shots_per_randomization': shots_per_randomization,
                    'num_randomizations': num_randomizations,
                    'layer_pair_depths': layer_pair_depths,
                },
            }
        }
        self.assert_valid_options(options)


    @combine(max_overhead=[0, 1, 18, None, "error"],
             noise_gain=[0, 1, 18, "auto", None, "error"],
             enable_pec_mitigation=[True, False],
             )
    def test_pec_mitigation_options(self, max_overhead, noise_gain, enable_pec_mitigation):
        """Testing various values of pec mitigation"""
        options = {
            'resilience': {
                'pec': {
                    'max_overhead': max_overhead,
                    'noise_gain': noise_gain,
                },
                'pec_mitigation': enable_pec_mitigation
            }
        }
        self.assert_valid_options(options)

    @combine(init_qubits=[True, False, 13],
             rep_delay=[0, 13, 0.3, -5, 'error'],
             )
    def test_execution_options(self, init_qubits, rep_delay):
        """Testing various values of execution options"""
        options = {
            'execution': {
                'init_qubits': init_qubits,
                'rep_delay': rep_delay,
            }
        }
        self.assert_valid_options(options)

    @combine(enable_gates=[True, False, 13],
             enable_measure=[True, False, 13],
             num_randomizations=[0, 1, 18, -3, "auto", None, "error"],
             shots_per_randomization=[0, 1, 18, -3, "auto", None, "error"],
             strategy=["active", "active-circuit", "active-accum", "all", "auto", "error", 42],
             )
    def test_twirling_options(self, enable_gates, enable_measure, num_randomizations, shots_per_randomization, strategy):
        """Testing various values of twirling options"""
        options = {
            'twirling': {
                'enable_gates': enable_gates,
                'enable_measure': enable_measure,
                'num_randomizations': num_randomizations,
                'shots_per_randomization': shots_per_randomization,
                'strategy': strategy,
            }
        }
        self.assert_valid_options(options)


@ddt.ddt
class TestSamplerV2Schema(unittest.TestCase):
    """Tests the sampler schema agrees with the format of the qiskit runtime sampler API calls"""
    def setUp(self) -> None:
        with open(os.path.join(SCHEMAS_PATH, 'sampler_v2_schema.json'), 'r') as fd:
            self.sampler_schema = json.load(fd)
        self.validator = jsonschema.Draft202012Validator(schema=self.sampler_schema)

    @staticmethod
    def get_converted_options(options_dict):
        """Emulate the process in `qiskit-ibm-runtime` where the EstimatorOptions
        are converted to a filtered options dictionary"""
        converted_options = SamplerOptions._get_program_inputs(options_dict)
        if 'pubs' not in converted_options:
            converted_options['pubs'] = []
        return converted_options

    def assert_valid_options(self, options_dict):
        """Verifies the schema validation gives the same result as attempting
        to set the options in the estimator"""
        converted_options = self.get_converted_options(options_dict)
        error_message = None
        options_valid = True
        try:
            self.validator.validate(converted_options)
        except Exception as err:
            options_valid = False
            error_message = str(err)

        sampler_options_valid = True
        try:
            SamplerOptions(**options_dict)
        except Exception as err:
            sampler_options_valid = False
            error_message = str(err)

        if sampler_options_valid:
            self.assertTrue(options_valid, msg=f"Options should pass the JSON schema validation, but it failed with the message:\n{error_message}")
        else:
            self.assertFalse(options_valid, msg=f"Options passed the JSON schema validation, but it should fail since for SamplerOptions it fails with the message:\n{error_message}")

    @ddt.data(0, 1, 3.5, -2)
    def test_default_shots(self, shots):
        """Testing various values of the default shots"""
        options = {'default_shots': shots}
        self.assert_valid_options(options)

    @combine(enable=[True, False, 13],
             sequence_type=["XX", "XpXm", "XY4", "ZZ", 13],
             extra_slack_distribution=["middle", "edges", "end", 13],
             scheduling_method=["alap", "asap", "lapsap", 13]
             )
    def test_dynamical_decoupling(self, enable, sequence_type, extra_slack_distribution, scheduling_method):
        """Testing various values of dynamical decoupling"""
        options = {
            'dynamical_decoupling': {
                'enable': enable,
                'sequence_type': sequence_type,
                'extra_slack_distribution': extra_slack_distribution,
                'scheduling_method': scheduling_method
            }
        }
        self.assert_valid_options(options)

    @combine(init_qubits=[True, False, 13],
             rep_delay=[0, 13, 0.3, -5, 'error'],
             )
    def test_execution_options(self, init_qubits, rep_delay):
        """Testing various values of execution options"""
        options = {
            'execution': {
                'init_qubits': init_qubits,
                'rep_delay': rep_delay,
            }
        }
        self.assert_valid_options(options)