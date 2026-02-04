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

"""Tests to check compliance of the models with the data, qiskit-ibm-runtime is actually sending."""

import json
from pathlib import Path

import pytest

from ibm_quantum_schemas.models.noise_learner_v2.version_0_1_dev.models import (
    OptionsModel,
    ParamsModel,
)

TEST_DATA_DIR = Path(__file__).parent / "test_data"


@pytest.mark.parametrize(
    "test_data_name,expected_num_circuits,expected_options",
    [
        (
            "minimum_input",
            0,
            {
                "max_layers_to_learn": 4,
                "shots_per_randomization": 128,
                "num_randomizations": 32,
                "layer_pair_depths": [0, 1, 2, 4, 16, 32],
                "twirling_strategy": "active-accum",
                "support_qiskit": True,
                "experimental": None,
                "simulator": None,
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
                "simulator": None,
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
                "simulator": None,
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
                "simulator": None,
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
                "simulator": None,
            },
        ),
        (
            "simulator_options",
            1,
            {
                "max_layers_to_learn": 4,
                "shots_per_randomization": 128,
                "num_randomizations": 32,
                "layer_pair_depths": [0, 1, 2, 4, 16, 32],
                "twirling_strategy": "active-accum",
                "support_qiskit": True,
                "experimental": None,
                "simulator": {
                    "seed_simulator": 42,
                    "coupling_map": [[0, 1], [1, 2]],
                    "basis_gates": ["u1", "u2", "u3", "cx"],
                    "noise_model": None,
                },
            },
        ),
    ],
)
def test_params_model_from_runtime_json(test_data_name, expected_num_circuits, expected_options):
    """Test that ParamsModel can deserialize RuntimeEncoder output."""
    # Load test data
    test_data_path = TEST_DATA_DIR / f"{test_data_name}.json"
    with open(test_data_path) as f:
        json_data = json.load(f)

    # Parse with ParamsModel
    params = ParamsModel.model_validate(json_data)

    # Verify schema version
    assert params.schema_version == "v0.1"

    # Verify number of circuits
    assert len(params.circuits) == expected_num_circuits

    # Verify all circuits are LegacyQpyModelV13to14
    from ibm_quantum_schemas.models.noise_learner_v2.version_0_1_dev.models import (
        CircuitQpyModelV13to14,
    )

    for circuit_model in params.circuits:
        assert isinstance(circuit_model, CircuitQpyModelV13to14)
        assert circuit_model.type_ == "QuantumCircuit"
        assert isinstance(circuit_model.value, str)
        assert len(circuit_model.value) > 0

    # Verify options
    assert isinstance(params.options, OptionsModel)
    from ibm_quantum_schemas.models.noise_learner_v2.version_0_1_dev.models import (
        SimulatorOptionsModel,
    )

    for key, expected_value in expected_options.items():
        actual_value = getattr(params.options, key)
        # Special handling for simulator field which is a SimulatorOptionsModel
        if key == "simulator" and expected_value is not None:
            assert isinstance(actual_value, SimulatorOptionsModel)
            for sim_key, sim_expected in expected_value.items():
                sim_actual = getattr(actual_value, sim_key)
                assert (
                    sim_actual == sim_expected
                ), f"Simulator option {sim_key}: expected {sim_expected}, got {sim_actual}"
        else:
            assert (
                actual_value == expected_value
            ), f"Option {key}: expected {expected_value}, got {actual_value}"


@pytest.mark.parametrize(
    "strategy",
    ["active", "active_circuit", "active_accum", "all"],
)
def test_twirling_strategies(strategy):
    """Test all twirling strategy variations."""
    test_data_name = f"strategy_{strategy}"
    test_data_path = TEST_DATA_DIR / f"{test_data_name}.json"

    with open(test_data_path) as f:
        json_data = json.load(f)

    params = ParamsModel.model_validate(json_data)

    # Verify schema version
    assert params.schema_version == "v0.1"

    # Verify strategy is set correctly (convert underscore back to hyphen)
    expected_strategy = strategy.replace("_", "-")
    assert params.options.twirling_strategy == expected_strategy
