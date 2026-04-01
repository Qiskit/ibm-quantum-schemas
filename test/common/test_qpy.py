# This code is a Qiskit project.
#
# (C) Copyright IBM 2025, 2026.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Tests for QPY models."""

from io import BytesIO

import pytest
from pybase64 import b64encode
from qiskit.circuit import QuantumCircuit
from qiskit.qpy import dump
from samplomatic import ChangeBasis, InjectNoise, Twirl

from ibm_quantum_schemas.common.qpy import (
    QpyDataV13ToV17Model,
    QpyModelV13ToV16,
    QpyModelV13ToV17,
    extract_qpy_info,
)


@pytest.mark.parametrize("qpy_version", [15, 16])
@pytest.mark.parametrize("num_circuits", [1, 3])
def test_extract_qpy_info(qpy_version, num_circuits):
    """Test the ``extract_qpy_info`` function."""
    circuit = QuantumCircuit(3)
    circuit.measure_all()

    with BytesIO() as bytes_buf:
        dump([circuit] * num_circuits, bytes_buf, version=qpy_version)
        qpy_str = b64encode(bytes_buf.getvalue()).decode()

    info = extract_qpy_info(qpy_str)
    assert info.qpy_version == qpy_version
    assert info.num_programs == num_circuits


class TestQpyModelV13ToV16:
    """Tests for ``QpyModelV13ToV16``."""

    @pytest.mark.skip_if_qiskit_too_old_for_qpy
    @pytest.mark.parametrize("qpy_version", [13, 14, 15, 16])
    def test_roundtrip(self, qpy_version):
        """Test that round trips work correctly."""
        circuit = QuantumCircuit(3)
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure_all()

        encoded = QpyModelV13ToV16.from_quantum_circuit(circuit, qpy_version)
        circuit_out = encoded.to_quantum_circuit()

        assert circuit == circuit_out

    @pytest.mark.skip_if_qiskit_too_old_for_qpy
    @pytest.mark.parametrize("qpy_version", [15, 16])
    def test_roundtrip_with_annotations(self, qpy_version):
        """Test that round trips work correctly for circuits with annotated boxes."""
        circuit = QuantumCircuit(3)
        circuit.h(0)
        circuit.cx(0, 1)
        with circuit.box([Twirl(), InjectNoise("ref"), ChangeBasis()]):
            circuit.cx(1, 2)
        circuit.measure_all()

        encoded = QpyModelV13ToV16.from_quantum_circuit(circuit, qpy_version)
        circuit_out = encoded.to_quantum_circuit()

        assert circuit == circuit_out

    @pytest.mark.parametrize("qpy_version", [12, 17])
    def test_unsupported_versions_raise(self, qpy_version):
        """Test that unsupported versions raise."""
        circuit = QuantumCircuit(3)
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure_all()

        with pytest.raises(ValueError):
            QpyModelV13ToV16.from_quantum_circuit(circuit, qpy_version)


class TestQpyModelV13ToV17:
    """Tests for ``QpyModelV13ToV17``."""

    @pytest.mark.skip_if_qiskit_too_old_for_qpy
    @pytest.mark.parametrize("qpy_version", [13, 14, 15, 16, 17])
    def test_roundtrip(self, qpy_version):
        """Test that round trips work correctly."""
        circuit = QuantumCircuit(3)
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure_all()

        encoded = QpyModelV13ToV17.from_quantum_circuit(circuit, qpy_version)
        circuit_out = encoded.to_quantum_circuit()

        assert circuit == circuit_out

    @pytest.mark.skip_if_qiskit_too_old_for_qpy
    @pytest.mark.parametrize("qpy_version", [15, 16, 17])
    def test_roundtrip_with_annotations(self, qpy_version):
        """Test that round trips work correctly for circuits with annotated boxes."""
        circuit = QuantumCircuit(3)
        circuit.h(0)
        circuit.cx(0, 1)
        with circuit.box([Twirl(), InjectNoise("ref"), ChangeBasis()]):
            circuit.cx(1, 2)
        circuit.measure_all()

        encoded = QpyModelV13ToV17.from_quantum_circuit(circuit, qpy_version)
        circuit_out = encoded.to_quantum_circuit()

        assert circuit == circuit_out

    @pytest.mark.parametrize("qpy_version", [12, 18])
    def test_unsupported_versions_raise(self, qpy_version):
        """Test that unsupported versions raise."""
        circuit = QuantumCircuit(3)
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure_all()

        with pytest.raises(ValueError):
            QpyModelV13ToV17.from_quantum_circuit(circuit, qpy_version)


class TestQpyDataV13ToV17Model:
    """Tests for ``QpyModelV13ToV17``."""

    @pytest.mark.skip_if_qiskit_too_old_for_qpy
    @pytest.mark.parametrize("qpy_version", [13, 14, 15, 16, 17])
    def test_roundtrip(self, qpy_version):
        """Test that round trips work correctly."""
        circuit0 = QuantumCircuit(3)
        circuit0.h(0)
        circuit0.cx(0, 1)
        circuit0.measure_all()

        circuit1 = QuantumCircuit(2)
        circuit1.h(0)
        circuit1.measure_all()

        circuits = [circuit0, circuit1]

        encoded = QpyDataV13ToV17Model[QuantumCircuit].from_python(circuits, qpy_version)

        assert encoded.num_programs == 2
        assert encoded.qpy_version == qpy_version

        circuits_out = encoded.to_python()

        assert circuits == circuits_out

    @pytest.mark.skip_if_qiskit_too_old_for_qpy
    @pytest.mark.parametrize("qpy_version", [15, 16, 17])
    def test_roundtrip_with_annotations(self, qpy_version):
        """Test that round trips work correctly for circuits with annotated boxes."""
        circuit = QuantumCircuit(3)
        circuit.h(0)
        circuit.cx(0, 1)
        with circuit.box([Twirl(), InjectNoise("ref"), ChangeBasis()]):
            circuit.cx(1, 2)
        circuit.measure_all()

        encoded = QpyDataV13ToV17Model.from_python([circuit], qpy_version)
        circuits_out = encoded.to_python()

        assert len(circuits_out) == 1
        assert circuit == circuits_out[0]

    @pytest.mark.parametrize("qpy_version", [12, 18])
    def test_unsupported_versions_raise(self, qpy_version):
        """Test that unsupported versions raise."""
        circuit = QuantumCircuit(3)
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure_all()

        with pytest.raises(ValueError):
            QpyDataV13ToV17Model.from_python([circuit], qpy_version)
