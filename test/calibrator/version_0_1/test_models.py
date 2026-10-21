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

"""Tests for 0.1 models."""

import datetime

from ibm_quantum_schemas.calibrator.version_0_1 import (
    CalibratorResultModel,
    OptionsModel,
    ParamsModel,
)


def test_initialization_params_model():
    """Test initialization for ``ParamsModel``."""
    options = OptionsModel()
    params_model = ParamsModel(options=options)

    assert params_model.schema_version == "v0.1"
    assert params_model.options == options


def test_initialization_results_model():
    """Test initialization for ``CalibratorResultModel``."""
    now = datetime.datetime.now()
    later = now + datetime.timedelta(seconds=5)
    results = CalibratorResultModel(start=now, stop=later)

    assert results.schema_version == "v0.1"
    assert results.start == now
    assert results.stop == later


def test_options_model_experimental():
    """Test ``OptionsModel`` experimental field with nested JSON values."""
    options = OptionsModel()
    assert options.experimental == {}

    nested_data = {
        "feature_flag": True,
        "foo": 0.5,
        "config": {
            "nested_list": [1, 2, {"deep": "value"}],
            "nested_bool": False,
        },
    }
    options = OptionsModel(experimental=nested_data)
    assert options.experimental == nested_data
