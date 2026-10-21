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

"""Tests for 0.2 models."""

import datetime

from ibm_quantum_schemas.calibrator.version_0_2_dev import (
    CalibratorResultModel,
    OneAndTwoQubitOptions,
    OptionsModel,
    ParamsModel,
    ReadoutAngleOptions,
    TlsBiasOptions,
    TwoQubitFractionalOptions,
    TwoQubitOptions,
)


def test_initialization_params_model():
    """Test initialization for ``ParamsModel``."""
    options = OptionsModel()
    params_model = ParamsModel(options=options)

    assert params_model.schema_version == "v0.2"
    assert params_model.options == options


def test_initialization_results_model():
    """Test initialization for ``CalibratorResultModel``."""
    now = datetime.datetime.now()
    later = now + datetime.timedelta(seconds=5)
    results = CalibratorResultModel(start=now, stop=later)

    assert results.schema_version == "v0.2"
    assert results.start == now
    assert results.stop == later


def test_options_model_defaults():
    """Test ``OptionsModel`` default values."""
    options = OptionsModel()

    assert options.readout_angle == ReadoutAngleOptions()
    assert options.one_and_two_qubit == OneAndTwoQubitOptions()
    assert options.two_qubit == TwoQubitOptions()
    assert options.two_qubit_fractional == TwoQubitFractionalOptions()
    assert options.tls_bias == TlsBiasOptions()
    assert options.experimental == {}


def test_options_model_experimental():
    """Test ``OptionsModel`` experimental field with nested JSON values."""
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


def test_readout_angle_options_defaults():
    """Test ``ReadoutAngleOptions`` default values."""
    opts = ReadoutAngleOptions()
    assert opts.enable is True


def test_readout_angle_options_disable():
    """Test ``ReadoutAngleOptions`` can be disabled."""
    opts = ReadoutAngleOptions(enable=False)
    assert opts.enable is False


def test_one_and_two_qubit_options_defaults():
    """Test ``OneAndTwoQubitOptions`` default values."""
    assert OneAndTwoQubitOptions().enable is False


def test_two_qubit_options_defaults():
    """Test ``TwoQubitOptions`` default values."""
    assert TwoQubitOptions().enable is False


def test_two_qubit_fractional_options_defaults():
    """Test ``TwoQubitFractionalOptions`` default values."""
    assert TwoQubitFractionalOptions().enable is False


def test_tls_bias_options_defaults():
    """Test ``TlsBiasOptions`` default values."""
    assert TlsBiasOptions().enable is False


def test_options_model_override_nested():
    """Test ``OptionsModel`` with non-default nested option values."""
    options = OptionsModel(
        readout_angle=ReadoutAngleOptions(enable=False),
        one_and_two_qubit=OneAndTwoQubitOptions(enable=True),
        two_qubit=TwoQubitOptions(enable=True),
        two_qubit_fractional=TwoQubitFractionalOptions(enable=True),
        tls_bias=TlsBiasOptions(enable=True),
    )

    assert options.readout_angle.enable is False
    assert options.one_and_two_qubit.enable is True
    assert options.two_qubit.enable is True
    assert options.two_qubit_fractional.enable is True
    assert options.tls_bias.enable is True
