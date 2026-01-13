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

import numpy as np
import pytest
from qiskit.circuit import Parameter, QuantumCircuit
from samplomatic import Twirl, build

from ibm_quantum_schemas.models.executor.version_0_2.models import (
    ChunkPart,
    ChunkSpan,
    CircuitItemModel,
    ItemMetadataModel,
    MetadataModel,
    OptionsModel,
    ParamsModel,
    QuantumProgramModel,
    QuantumProgramResultItemModel,
    QuantumProgramResultModel,
    SamplexItemModel,
    SchedulerTimingModel,
    StretchValueModel,
)
from ibm_quantum_schemas.models.qpy_model import QpyModelV13ToV17
from ibm_quantum_schemas.models.samplex_model import SamplexModelSSV1ToSSV2 as SamplexModel
from ibm_quantum_schemas.models.tensor_model import F64TensorModel, TensorModel


@pytest.mark.skip_if_qiskit_too_old_for_qpy
@pytest.mark.skip_if_samplomatic_too_old_for_ssv
@pytest.mark.parametrize(
    "qpy_version,ssv,chunk_size",
    [(13, 2, 2), (14, 1, 2), (15, 2, 2), (16, 1, 2), (17, 2, 2), (16, 1, "auto"), (16, 2, "auto")],
)
def test_initialization_params_model(qpy_version, ssv, chunk_size):
    """Test initialization for ``ParamsModel`` and related models."""
    options = OptionsModel()

    circuit = QuantumCircuit(3)
    circuit.rx(Parameter("theta"), 0)
    circuit.rz(Parameter("phi"), 0)
    circuit.rx(Parameter("lam"), 0)
    circuit.cx(0, 1)
    circuit.measure_all()
    circuit_item = CircuitItemModel(
        circuit=QpyModelV13ToV17.from_quantum_circuit(circuit, qpy_version),
        circuit_arguments=F64TensorModel.from_numpy(np.array([0.1, 0.2, 0.3], dtype=np.float64)),
        chunk_size=chunk_size,
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
        circuit=QpyModelV13ToV17.from_quantum_circuit(template, qpy_version),
        samplex=SamplexModel.from_samplex(samplex, ssv=ssv),
        samplex_arguments={
            "parameter_values": TensorModel.from_numpy(np.array([0.1, 0.2, 0.3], dtype=np.float64))
        },
        shape=(200, 300),
        chunk_size=chunk_size,
    )

    quantum_program = QuantumProgramModel(shots=1000, items=[circuit_item, samplex_item])
    params_model = ParamsModel(quantum_program=quantum_program, options=options)

    assert params_model.schema_version == "v0.2"
    assert params_model.quantum_program == quantum_program
    assert params_model.options == options
    assert quantum_program.meas_level == "classified"


def test_initialization_results_model():
    """Test initialization for ``QuantumProgramResultModel`` and related models."""
    result_item = QuantumProgramResultItemModel(
        results={
            "alpha": TensorModel.from_numpy(np.array([0.1, 0.2], dtype=np.float64)),
            "beta": TensorModel.from_numpy(np.array([0.3, 0.4, 0.5], dtype=np.float64)),
        },
        metadata=ItemMetadataModel(),
    )
    now = datetime.datetime.now()
    spans = [
        ChunkSpan(
            start=now,
            stop=now + datetime.timedelta(seconds=5.1),
            parts=[ChunkPart(idx_item=0, size=5)],
        )
    ]
    metadata = MetadataModel(chunk_timing=spans)
    results = QuantumProgramResultModel(data=[result_item], metadata=metadata)

    assert results.schema_version == "v0.2"
    assert results.data == [result_item]
    assert results.metadata == metadata


def test_chunk_size_validation():
    """Test initialization for ``ParamsModel`` and related models."""
    circuit = QuantumCircuit(3)
    circuit_item = CircuitItemModel(
        circuit=QpyModelV13ToV17.from_quantum_circuit(circuit, 16),
        circuit_arguments=F64TensorModel.from_numpy(np.array([], dtype=np.float64)),
        chunk_size=2,
    )

    template, samplex = build(circuit)
    samplex_item = SamplexItemModel(
        circuit=QpyModelV13ToV17.from_quantum_circuit(template, 16),
        samplex=SamplexModel.from_samplex(samplex, ssv=1),
        samplex_arguments={
            "parameter_values": TensorModel.from_numpy(np.array([], dtype=np.float64))
        },
        shape=(),
        chunk_size="auto",
    )

    with pytest.raises(ValueError, match="all items must specify one or the other"):
        QuantumProgramModel(shots=1000, items=[circuit_item, samplex_item])


@pytest.mark.parametrize("meas_level", ["classified", "kerneled", "avg_kerneled"])
def test_meas_level(meas_level):
    """Test that meas_level can be set to all valid values."""
    circuit = QuantumCircuit(3)
    circuit.measure_all()
    circuit_item = CircuitItemModel(
        circuit=QpyModelV13ToV17.from_quantum_circuit(circuit, 16),
        circuit_arguments=F64TensorModel.from_numpy(np.array([], dtype=np.float64)),
    )

    quantum_program = QuantumProgramModel(shots=100, items=[circuit_item], meas_level=meas_level)

    assert quantum_program.meas_level == meas_level


def test_options_model_scheduler_timing_and_stretch_values():
    """Test OptionsModel with scheduler_timing and stretch_values fields."""
    options = OptionsModel()
    assert not options.scheduler_timing
    assert not options.stretch_values

    options = OptionsModel(scheduler_timing=True)
    assert options.scheduler_timing
    assert not options.stretch_values

    options = OptionsModel(stretch_values=True)
    assert not options.scheduler_timing
    assert options.stretch_values

    options = OptionsModel(scheduler_timing=True, stretch_values=True)
    assert options.scheduler_timing
    assert options.stretch_values


def test_scheduler_timing_model():
    """Test SchedulerTimingModel initialization and fields."""
    timing = SchedulerTimingModel(timing="0,100,200,300", circuit_duration=400)
    assert timing.timing == "0,100,200,300"
    assert timing.circuit_duration == 400


def test_stretch_value_model():
    """Test StretchValueModel initialization and fields."""
    stretch = StretchValueModel(
        name="delay_stretch",
        value=100,
        remainder=4,
        expanded_values=[(0, 100), (200, 104), (500, 100)],
    )
    assert stretch.name == "delay_stretch"
    assert stretch.value == 100
    assert stretch.remainder == 4
    assert stretch.expanded_values == [(0, 100), (200, 104), (500, 100)]


def test_result_item_with_metadata():
    """Test QuantumProgramResultItemModel with populated metadata."""
    scheduler_timing = SchedulerTimingModel(timing="0,100,200", circuit_duration=300)
    stretch = StretchValueModel(name="stretch_1", value=80, remainder=0, expanded_values=[(50, 80)])
    item_metadata = ItemMetadataModel(scheduler_timing=scheduler_timing, stretch_values=[stretch])

    result_item = QuantumProgramResultItemModel(
        results={
            "counts": TensorModel.from_numpy(np.array([100, 200], dtype=np.float64)),
        },
        metadata=item_metadata,
    )

    assert result_item.metadata.scheduler_timing == scheduler_timing
    assert result_item.metadata.stretch_values == [stretch]
