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

SCHEMAS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "schemas"
)

@ddt.ddt
class TestEstimatorV2OutputSchema(unittest.TestCase):
    """Tests the estimator output schema"""

    def setUp(self) -> None:
        with open(os.path.join(SCHEMAS_PATH, "estimator_v2_output_schema.json"), "r") as fd:
            self.estimator_schema = json.load(fd)
        self.validator = jsonschema.Draft202012Validator(schema=self.estimator_schema)

    def test_basic_output(self):
        output = '{"results": [{"data": {"evs": 1.1142546245919478, "stds": 0.012101383035893986, "ensemble_standard_error": 0.012101383035893986}, "metadata": {"shots": 4096, "target_precision": 0.015625, "circuit_metadata": {}, "resilience": {}, "num_randomizations": 32}}], "metadata": {"dynamical_decoupling": {"enable": false, "sequence_type": "XX", "extra_slack_distribution": "middle", "scheduling_method": "alap"}, "twirling": {"enable_gates": false, "enable_measure": true, "num_randomizations": "auto", "shots_per_randomization": "auto", "interleave_randomizations": true, "strategy": "active-accum"}, "resilience": {"measure_mitigation": true, "zne_mitigation": false, "pec_mitigation": false}, "version": 2}}'

class TestSamplerV2OutputSchema(unittest.TestCase):
    """Tests the sampler output schema"""

    def setUp(self) -> None:
        with open(os.path.join(SCHEMAS_PATH, "sampler_v2_output_schema.json"), "r") as fd:
            self.sampler_schema = json.load(fd)
        self.validator = jsonschema.Draft202012Validator(schema=self.sampler_schema)

    def test_basic_output(self):
        output = '{"results": [{"data": {"meas": {"samples": ["0x3", "0x3", "0x3", "0x3", "0x3"], "num_bits": 2}}, "metadata": {"circuit_metadata": {}}}], "metadata": {"version": 2}}'
