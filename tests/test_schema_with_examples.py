# This code is part of Qiskit.
#
# (C) Copyright IBM 2020
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
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'schemas')
EXAMPLES_PATH = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'schemas', 'examples')


EXAMPLES = [
    ('backend_configuration_schema',
     'backend_configuration_openpulse_example'),
    ('backend_configuration_schema',
     'backend_configuration_openqasm_example'),
    ('backend_configuration_schema',
     'backend_configuration_openqasm_simulator_example'),
    ('backend_properties_schema', 'backend_properties_example'),
    ('backend_status_schema', 'backend_status_example'),
    ('default_pulse_configuration_schema',
     'default_pulse_configuration_example'),
    ('job_status_schema', 'job_status_example'),
    ('qobj_schema', 'qasm_w_pulse_gates'),
    ('qobj_schema', 'qobj_openpulse_example'),
    ('qobj_schema', 'qobj_openqasm_example'),
    ('result_schema', 'result_openpulse_level_0_example'),
    ('result_schema', 'result_openqasm_example'),
    ('result_schema', 'result_statevector_simulator_example'),
    ('result_schema', 'result_unitary_simulator_example')
]


@ddt.ddt
class TestJSONSchemaExamples(unittest.TestCase):

    @ddt.data(*EXAMPLES)
    @ddt.unpack
    def test_example(self, schema, example):
        schema_path = os.path.join(SCHEMAS_PATH, schema + '.json')
        examples_path = os.path.join(EXAMPLES_PATH, example + '.json')
        with open(schema_path, 'r') as schema_file:
            with open(examples_path, 'r') as example_file:
                self.assertIsNone(
                    jsonschema.validate(json.load(example_file),
                                        json.load(schema_file)))
