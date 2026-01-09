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

"""Tests for 0.2 models."""

import numpy as np
import pytest
from qiskit.circuit import QuantumCircuit

from ibm_quantum_schemas.models.noise_learner_v3.version_0_2.models import (
    LinbdbladResultMetadataModel,
    NoiseLearnerV3ResultModel,
    NoiseLearnerV3ResultsModel,
    OptionsModel,
    ParamsModel,
    PostSelectionMetadataModel,
    TREXResultMetadataModel,
)
from ibm_quantum_schemas.models.qpy_model import QpyModelV13ToV16
from ibm_quantum_schemas.models.tensor_model import F64TensorModel


@pytest.mark.parametrize("qpy_version", [13, 14, 15, 16])
def test_initialization_params_model(qpy_version):
    """Test initialization for ``ParamsModel`` and related models."""
    options = OptionsModel()

    circuit = QuantumCircuit(3)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure_all()
    instructions = QpyModelV13ToV16.from_quantum_circuit(circuit, qpy_version)

    params_model = ParamsModel(instructions=instructions, options=options)

    assert params_model.schema_version == "v0.2"
    assert params_model.instructions == instructions
    assert params_model.options == options


def test_initialization_results_model():
    """Test initialization for ``NoiseLearnerV3ResultsModel`` and related models."""
    lindblad_datum = NoiseLearnerV3ResultModel(
        generators_sparse=[[("XI", [0, 1]), ("XX", [1, 2])]],
        num_qubits=2,
        rates=F64TensorModel.from_numpy(np.array(range(2), dtype=np.float64)),
        rates_std=F64TensorModel.from_numpy(np.zeros((2,), dtype=np.float64)),
        metadata=LinbdbladResultMetadataModel(
            post_selection={
                0: PostSelectionMetadataModel(
                    fraction_kept=0.8, success_rates={0: 0.99, 1: 0.98, 2: 0.97}
                ),
                2: PostSelectionMetadataModel(
                    fraction_kept=0.8, success_rates={0: 0.89, 1: 0.88, 2: 0.87}
                ),
            }
        ),
    )

    trex_datum = NoiseLearnerV3ResultModel(
        generators_sparse=[[("X", [0]), ("X", [1])]],
        num_qubits=2,
        rates=F64TensorModel.from_numpy(np.array(range(2), dtype=np.float64)),
        rates_std=F64TensorModel.from_numpy(np.zeros((2,), dtype=np.float64)),
        metadata=TREXResultMetadataModel(
            post_selection=PostSelectionMetadataModel(
                fraction_kept=0.9, success_rates={0: 0.99, 1: 0.98, 2: 0.8}
            )
        ),
    )

    results = NoiseLearnerV3ResultsModel(data=[lindblad_datum, trex_datum])

    assert results.schema_version == "v0.2"
    assert results.data == [lindblad_datum, trex_datum]
