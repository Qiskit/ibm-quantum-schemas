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

"""Tests for 0.1 models."""

import numpy as np
import pytest
from qiskit.circuit import Parameter, QuantumCircuit
from samplomatic import Twirl, build

from ibm_quantum_schemas.models.execution_span_model import BasicExecutionSpan
from ibm_quantum_schemas.models.executor.version_0_1.models import (
    CircuitItemModel,
    MetadataModel,
    OptionsModel,
    ParamsModel,
    QuantumProgramModel,
    QuantumProgramResultItemModel,
    QuantumProgramResultModel,
    SamplexItemModel,
)
from ibm_quantum_schemas.models.qpy_model import QpyModelV13ToV16
from ibm_quantum_schemas.models.samplex_model import SamplexModel
from ibm_quantum_schemas.models.tensor_model import F64TensorModel, TensorModel


@pytest.mark.parametrize("qpy_version", [13, 14, 15, 16])
def test_initialization_params_model(qpy_version):
    """Test initialization for ``ParamsModel`` and related models."""
    options = OptionsModel()

    circuit = QuantumCircuit(3)
    circuit.rx(Parameter("theta"), 0)
    circuit.rz(Parameter("phi"), 0)
    circuit.rx(Parameter("lam"), 0)
    circuit.cx(0, 1)
    circuit.measure_all()
    circuit_item = CircuitItemModel(
        circuit=QpyModelV13ToV16.from_quantum_circuit(circuit, qpy_version),
        circuit_arguments=F64TensorModel.from_numpy(np.array([0.1, 0.2, 0.3], dtype=np.float64)),
        chunk_size=2,
    )

    circuit = QuantumCircuit(3)
    with circuit.box([Twirl()]):
        circuit.rx(Parameter("theta"), 0)
        circuit.rz(Parameter("phi"), 0)
        circuit.rx(Parameter("lam"), 0)
        circuit.cx(0, 1)
    with circuit.box([Twirl()]):
        circuit.measure_all()
    template, samplex = build(circuit)
    samplex_item = SamplexItemModel(
        circuit=QpyModelV13ToV16.from_quantum_circuit(template, qpy_version),
        samplex=SamplexModel.from_samplex(samplex),
        samplex_arguments={
            "parameter_values": TensorModel.from_numpy(np.array([0.1, 0.2, 0.3], dtype=np.float64))
        },
        shape=(200, 300),
        chunk_size=2,
    )

    quantum_program = QuantumProgramModel(shots=1000, items=[circuit_item, samplex_item])
    params_model = ParamsModel(quantum_program=quantum_program, options=options)

    assert params_model.schema_version == "v0.1"
    assert params_model.quantum_program == quantum_program
    assert params_model.options == options


def test_initialization_results_model():
    """Test initialization for ``QuantumProgramResultModel`` and related models."""
    result_item = QuantumProgramResultItemModel(
        results={
            "alpha": TensorModel.from_numpy(np.array([0.1, 0.2], dtype=np.float64)),
            "beta": TensorModel.from_numpy(np.array([0.3, 0.4, 0.5], dtype=np.float64)),
        },
        metadata=None,
    )
    metadata = MetadataModel(execution_spans=[BasicExecutionSpan(start=1, stop=2)])
    results = QuantumProgramResultModel(data=[result_item], metadata=metadata)

    assert results.schema_version == "v0.1"
    assert results.data == [result_item]
    assert results.metadata == metadata
