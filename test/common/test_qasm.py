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

"""Tests for OpenQASM3 models."""

from qiskit.circuit import Parameter, QuantumCircuit
from samplomatic import ChangeBasis, InjectNoise, Twirl

from ibm_quantum_schemas.common.qasm import OpenQasm3DataModel


class TestOpenQasm3DataModel:
    """Tests for ``OpenQasm3DataModel``."""

    def test_roundtrip(self):
        """Test that round trips work correctly."""
        circuit0 = QuantumCircuit(2)
        circuit0.h(0)
        circuit0.cx(0, 1)
        circuit0.measure_all()

        circuit1 = QuantumCircuit(2)
        circuit1.h(0)
        circuit1.measure_all()

        circuit2 = QuantumCircuit(1)
        circuit2.rx(Parameter("theta"), 0)

        circuits = [circuit0, circuit1, circuit2]

        encoded = OpenQasm3DataModel.from_python(circuits)
        circuits_out = encoded.to_python()
        assert circuits == circuits_out

        # testing direct initialization
        encoded_data = OpenQasm3DataModel(data=encoded.data)
        circuit0_out = encoded_data.to_python()[0]
        assert circuit0_out == circuit0

        encoded_num_qubits = OpenQasm3DataModel(data=encoded.data, num_qubits=encoded.num_qubits)
        circuit1_out = encoded_num_qubits.to_python()[1]
        assert circuit1_out == circuit1

    def test_roundtrip_with_annotations(self):
        """Test that round trips work correctly for circuits with annotated boxes."""
        circuit = QuantumCircuit(3)
        circuit.h(0)
        circuit.cx(0, 1)
        with circuit.box([Twirl(), InjectNoise("ref"), ChangeBasis()]):
            circuit.cx(1, 2)
        circuit.measure_all()

        encoded = OpenQasm3DataModel.from_python([circuit])
        circuits_out = encoded.to_python()

        assert len(circuits_out) == 1
        assert circuit == circuits_out[0]
