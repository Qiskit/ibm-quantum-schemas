# This code is a Qiskit project.
#
# (C) Copyright IBM 2025.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Tests for noise_learner_v2 version 0.1 models."""

import json
from pathlib import Path

import pytest
from qiskit.circuit import QuantumCircuit

from ibm_quantum_schemas.models.noise_learner_v2.version_0_1.models import (
    OptionsModel,
    ParamsModel,
)
from ibm_quantum_schemas.models.qpy_model import QpyModelV13ToV16


FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.mark.parametrize(
    "fixture_name,expected_num_circuits,expected_options",
    [
        (
            "basic_single_circuit",
            1,
            {
                "max_layers_to_learn": 4,
                "shots_per_randomization": 128,
                "num_randomizations": 32,
                "layer_pair_depths": [0, 1, 2, 4, 16, 32],
                "twirling_strategy": "active-accum",
                "support_qiskit": True,
                "experimental": None,
            },
        ),
        (
            "multiple_circuits",
            3,
            {
                "max_layers_to_learn": 4,
                "shots_per_randomization": 128,
                "num_randomizations": 32,
                "layer_pair_depths": [0, 1, 2, 4, 16, 32],
                "twirling_strategy": "active-accum",
                "support_qiskit": True,
                "experimental": None,
            },
        ),
        (
            "custom_options",
            1,
            {
                "max_layers_to_learn": 10,
                "shots_per_randomization": 256,
                "num_randomizations": 64,
                "layer_pair_depths": [0, 2, 8, 16],
                "twirling_strategy": "active-circuit",
                "support_qiskit": True,
                "experimental": None,
            },
        ),
        (
            "none_max_layers",
            1,
            {
                "max_layers_to_learn": 4,  # Defaults to 4 when not present in JSON
                "shots_per_randomization": 128,
                "num_randomizations": 32,
                "layer_pair_depths": [0, 1, 2, 4, 16, 32],
                "twirling_strategy": "active-accum",
                "support_qiskit": True,
                "experimental": None,
            },
        ),
        (
            "experimental_options",
            1,
            {
                "max_layers_to_learn": 4,
                "shots_per_randomization": 128,
                "num_randomizations": 32,
                "layer_pair_depths": [0, 1, 2, 4, 16, 32],
                "twirling_strategy": "active-accum",
                "support_qiskit": True,
                "experimental": {"some_flag": True, "test_value": 42},
            },
        ),
    ],
)
def test_params_model_from_runtime_json(fixture_name, expected_num_circuits, expected_options):
    """Test that ParamsModel can deserialize RuntimeEncoder output."""
    # Load fixture
    fixture_path = FIXTURES_DIR / f"{fixture_name}.json"
    with open(fixture_path) as f:
        json_data = json.load(f)
    
    # Parse with ParamsModel
    params = ParamsModel.model_validate(json_data)
    
    # Verify schema version
    assert params.schema_version == "v0.1"
    
    # Verify number of circuits
    assert len(params.circuits) == expected_num_circuits
    
    # Verify all circuits are LegacyQpyModelV13to14
    from ibm_quantum_schemas.models.noise_learner_v2.version_0_1.models import CircuitQpyModelV13to14
    for circuit_model in params.circuits:
        assert isinstance(circuit_model, CircuitQpyModelV13to14)
        assert circuit_model.type_ == "QuantumCircuit"
        assert isinstance(circuit_model.value, str)
        assert len(circuit_model.value) > 0
    
    # Verify options
    assert isinstance(params.options, OptionsModel)
    for key, expected_value in expected_options.items():
        actual_value = getattr(params.options, key)
        assert actual_value == expected_value, f"Option {key}: expected {expected_value}, got {actual_value}"


@pytest.mark.parametrize(
    "strategy",
    ["active", "active_circuit", "active_accum", "all"],
)
def test_twirling_strategies(strategy):
    """Test all twirling strategy variations."""
    fixture_name = f"strategy_{strategy}"
    fixture_path = FIXTURES_DIR / f"{fixture_name}.json"
    
    with open(fixture_path) as f:
        json_data = json.load(f)
    
    params = ParamsModel.model_validate(json_data)
    
    # Verify schema version
    assert params.schema_version == "v0.1"
    
    # Verify strategy is set correctly (convert underscore back to hyphen)
    expected_strategy = strategy.replace("_", "-")
    assert params.options.twirling_strategy == expected_strategy


def test_options_model_defaults():
    """Test OptionsModel with default values."""
    options = OptionsModel()
    
    assert options.max_layers_to_learn == 4
    assert options.shots_per_randomization == 128
    assert options.num_randomizations == 32
    assert options.layer_pair_depths == [0, 1, 2, 4, 16, 32]
    assert options.twirling_strategy == "active-accum"
    assert options.support_qiskit is True
    assert options.experimental is None


def test_options_model_custom_values():
    """Test OptionsModel with custom values."""
    options = OptionsModel(
        max_layers_to_learn=10,
        shots_per_randomization=256,
        num_randomizations=64,
        layer_pair_depths=[0, 2, 8],
        twirling_strategy="active",
        experimental={"test": True},
    )
    
    assert options.max_layers_to_learn == 10
    assert options.shots_per_randomization == 256
    assert options.num_randomizations == 64
    assert options.layer_pair_depths == [0, 2, 8]
    assert options.twirling_strategy == "active"
    assert options.experimental == {"test": True}

# Made with Bob
