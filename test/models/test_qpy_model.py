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

"""Tests for QPY models."""

import pytest
from qiskit.circuit import QuantumCircuit
from samplomatic import ChangeBasis, InjectNoise, Twirl

from ibm_quantum_schemas.models.qpy_model import QpyModelV13ToV16, QpyModelV13ToV17


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
