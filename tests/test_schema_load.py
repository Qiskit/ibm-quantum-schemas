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
import fastjsonschema
import jsonschema_rs

LOADERS = [fastjsonschema.compile,
           jsonschema_rs.JSONSchema]

SCHEMAS_PATH = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'schemas')


@ddt.ddt
class TestFastJSONSchemaLoad(unittest.TestCase):

    @ddt.data(*LOADERS)
    def test_backend_configuration_load(self, loader):
        with open(os.path.join(SCHEMAS_PATH,
                               'backend_configuration_schema.json'),
                  'r') as fd:
            self.assertIsNotNone(loader(json.load(fd)))

    @ddt.data(*LOADERS)
    def test_backend_properties_load(self, loader):
        with open(os.path.join(SCHEMAS_PATH,
                               'backend_properties_schema.json'),
                  'r') as fd:
            self.assertIsNotNone(loader(json.load(fd)))

    @ddt.data(*LOADERS)
    def test_backend_status_load(self, loader):
        with open(os.path.join(SCHEMAS_PATH,
                               'backend_status_schema.json'),
                  'r') as fd:
            self.assertIsNotNone(loader(json.load(fd)))

    @ddt.data(*LOADERS)
    def test_default_pulse_config_load(self, loader):
        with open(os.path.join(SCHEMAS_PATH,
                               'default_pulse_configuration_schema.json'),
                  'r') as fd:
            self.assertIsNotNone(loader(json.load(fd)))

    @ddt.data(*LOADERS)
    def test_ibmq_device_qobj_load(self, loader):
        with open(os.path.join(SCHEMAS_PATH,
                               'ibmq_device_qobj_schema.json'),
                  'r') as fd:
            self.assertIsNotNone(loader(json.load(fd)))

    @ddt.data(*LOADERS)
    def test_ibmq_simulator_qobj_schema_load(self, loader):
        with open(os.path.join(SCHEMAS_PATH,
                               'ibmq_simulator_qobj_schema.json'),
                  'r') as fd:
            self.assertIsNotNone(loader(json.load(fd)))

    @ddt.data(*LOADERS)
    def test_job_status_load(self, loader):
        with open(os.path.join(SCHEMAS_PATH,
                               'job_status_schema.json'),
                  'r') as fd:
            self.assertIsNotNone(loader(json.load(fd)))

    @ddt.data(*LOADERS)
    def test_qobj_load(self, loader):
        with open(os.path.join(SCHEMAS_PATH,
                               'qobj_schema.json'),
                  'r') as fd:
            self.assertIsNotNone(loader(json.load(fd)))

    @ddt.data(*LOADERS)
    def test_result_schema_load(self, loader):
        with open(os.path.join(SCHEMAS_PATH,
                               'result_schema.json'),
                  'r') as fd:
            self.assertIsNotNone(loader(json.load(fd)))


class TestJSONSchemaLoad(unittest.TestCase):

    def test_backend_configuration_load(self,):
        with open(os.path.join(SCHEMAS_PATH,
                               'backend_configuration_schema.json'),
                  'r') as fd:
            self.assertIsNone(jsonschema.Draft4Validator.check_schema(
                json.load(fd)))

    def test_backend_properties_load(self):
        with open(os.path.join(SCHEMAS_PATH,
                               'backend_properties_schema.json'),
                  'r') as fd:
            self.assertIsNone(jsonschema.Draft4Validator.check_schema(
                json.load(fd)))

    def test_backend_status_load(self):
        with open(os.path.join(SCHEMAS_PATH,
                               'backend_status_schema.json'),
                  'r') as fd:
            self.assertIsNone(jsonschema.Draft4Validator.check_schema(
                json.load(fd)))

    def test_default_pulse_config_load(self):
        with open(os.path.join(SCHEMAS_PATH,
                               'default_pulse_configuration_schema.json'),
                  'r') as fd:
            self.assertIsNone(jsonschema.Draft4Validator.check_schema(
                json.load(fd)))

    def test_ibmq_device_qobj_load(self):
        with open(os.path.join(SCHEMAS_PATH,
                               'ibmq_device_qobj_schema.json'),
                  'r') as fd:
            self.assertIsNone(jsonschema.Draft4Validator.check_schema(
                json.load(fd)))

    def test_ibmq_simulator_qobj_schema_load(self):
        with open(os.path.join(SCHEMAS_PATH,
                               'ibmq_simulator_qobj_schema.json'),
                  'r') as fd:
            self.assertIsNone(jsonschema.Draft4Validator.check_schema(
                json.load(fd)))

    def test_job_status_load(self):
        with open(os.path.join(SCHEMAS_PATH,
                               'job_status_schema.json'),
                  'r') as fd:
            self.assertIsNone(jsonschema.Draft4Validator.check_schema(
                json.load(fd)))

    def test_qobj_load(self):
        with open(os.path.join(SCHEMAS_PATH,
                               'qobj_schema.json'),
                  'r') as fd:
            self.assertIsNone(jsonschema.Draft4Validator.check_schema(
                json.load(fd)))

    def test_result_schema_load(self):
        with open(os.path.join(SCHEMAS_PATH,
                               'result_schema.json'),
                  'r') as fd:
            self.assertIsNone(jsonschema.Draft4Validator.check_schema(
                json.load(fd)))
