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
from dataclasses import asdict
import jsonschema


from qiskit_ibm_runtime import SamplerV2, EstimatorV2

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
        self.backend = "ibmq_qasm_simulator"

    @staticmethod
    def get_options_dict(estimator):
        """Emulate the process in `qiskit-ibm-runtime` where the EstimatorOptions
        are converted to a filtered options dictionary"""
        options_dict = estimator.options._get_program_inputs(asdict(estimator.options))
        if 'pubs' not in options_dict:
            options_dict['pubs'] = []
        return options_dict

    def assert_valid_options(self, estimator, options_to_check, options_path=""):
        """Verifies the schema validation gives the same result as attempting
        to set the options in the estimator"""
        options = estimator.options
        try:
            for option_name, value in options_to_check.items():
                setattr(options, option_name, value)
            options_dict = TestEstimatorV2Schema.get_options_dict(estimator)
            self.assertTrue(self.validator.is_valid(options_dict))
        except Exception:
            options_dict = TestEstimatorV2Schema.get_options_dict(estimator)
            for option_name, value in options_to_check.items():
                dict_to_change = options_dict
                for key in options_path:
                    dict_to_change = dict_to_change[key]
                dict_to_change[option_name] = value
            self.assertFalse(self.validator.is_valid(options_dict))
    def test_basic(self):
        """Testing the bare-bones options for an estimator"""
        estimator = EstimatorV2(backend=self.backend)
        options = self.get_options_dict(estimator)
        self.assertIsNone(self.validator.validate(options))

    @ddt.data(0, 1, 2, 3, -1, 17, 3.5)
    def test_resilience_level(self, level):
        """Testing various values of the resilience level"""
        estimator = EstimatorV2(backend=self.backend)
        options_to_set = {'resilience_level': level}
        self.assert_valid_options(estimator, options_to_set)

    @ddt.data(0, 1, 3.5)
    def test_seed_estimator(self, seed):
        """Testing various values of the seed estimator"""
        estimator = EstimatorV2(backend=self.backend)
        options_path = ['options']
        options_to_set = {'seed_estimator': seed}
        self.assert_valid_options(estimator, options_to_set, options_path)

    @ddt.data(0, 1, 3.5)
    def test_default_precision(self, precision):
        """Testing various values of the default precision"""
        estimator = EstimatorV2(backend=self.backend)
        options_path = ['options']
        options_to_set = {'default_precision': precision}
        self.assert_valid_options(estimator, options_to_set, options_path)

    @ddt.data(0, 1, 3.5, -2)
    def test_default_shots(self, shots):
        """Testing various values of the default shots"""
        estimator = EstimatorV2(backend=self.backend)
        options_path = ['options']
        options_to_set = {'default_shots': shots}
        self.assert_valid_options(estimator, options_to_set, options_path)
