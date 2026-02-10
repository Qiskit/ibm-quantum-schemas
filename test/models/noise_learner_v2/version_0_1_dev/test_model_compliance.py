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

"""Tests to check compliance of the models with the data, qiskit-ibm-runtime is actually sending.

This is a temporary test while qiskit-ibm-runtime is still using its own conversion code.
Once qiskit-ibm-runtime uses ibm-quantum-schemas as a source of truth, compliance is implicitly
ensured and we can remove the tests in this file.
"""

import json
from pathlib import Path

from ibm_quantum_schemas.models.noise_learner_v2.version_0_1_dev.models import ResultsModel

TEST_DATA_DIR = Path(__file__).parent / "test_data"


def test_result_model_from_runtime_json():
    """Test that ResultsModel can deserialize RuntimeEncoder output."""
    # Load test data
    test_data_path = TEST_DATA_DIR / "result_example.json"
    with open(test_data_path) as f:
        json_data = json.load(f)

    # Parse with ResultsModel
    result = ResultsModel.model_validate(json_data)

    # Verify schema version
    assert result.schema_version == "v0.1"

    # Verify data contains LayerNoiseWrapperModel instances
    from ibm_quantum_schemas.models.noise_learner_v2.version_0_1_dev.layer_noise_model import (
        LayerNoiseWrapperModel,
    )

    assert len(result.data) == 4
    for layer_noise in result.data:
        assert isinstance(layer_noise, LayerNoiseWrapperModel)
        # Verify each LayerNoiseWrapperModel has the wrapper structure
        assert layer_noise.type_ == "_json"
        assert layer_noise.module_ == "qiskit_ibm_runtime.utils.noise_learner_result"
        assert layer_noise.class_ == "LayerError"

        # Verify the value_ contains the actual data
        assert hasattr(layer_noise.value_, "circuit")
        assert hasattr(layer_noise.value_, "qubits")
        assert hasattr(layer_noise.value_, "error")
        assert isinstance(layer_noise.value_.qubits, list)
        assert all(isinstance(q, int) for q in layer_noise.value_.qubits)

        # Verify circuit is properly encoded
        from ibm_quantum_schemas.models.noise_learner_v2.version_0_1_dev import (
            circuit_qpy_model_v13_to_v17 as qpy_model,
        )

        assert isinstance(layer_noise.value_.circuit, qpy_model.CircuitQpyModelV13to17)
        assert layer_noise.value_.circuit.type_ == "QuantumCircuit"

    # Verify metadata
    from ibm_quantum_schemas.models.noise_learner_v2.version_0_1_dev.results_metadata_model import (
        ResultsMetadataModel,
    )

    assert isinstance(result.metadata, ResultsMetadataModel)
    assert result.metadata.backend == "aer_simulator"
    assert result.metadata.input_options is not None
    assert result.metadata.input_options.max_layers_to_learn == 4
    assert result.metadata.input_options.shots_per_randomization == 128
    assert result.metadata.input_options.num_randomizations == 32
    assert result.metadata.input_options.layer_pair_depths == [0, 1, 2, 4, 16, 32]
    assert result.metadata.input_options.twirling_strategy == "active-accum"
