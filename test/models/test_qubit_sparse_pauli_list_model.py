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

"""Tests for samplex models."""

from qiskit.quantum_info import QubitSparsePauliList

from ibm_quantum_schemas.models.qubit_sparse_pauli_list_model import QubitSparsePauliListModel


def test_roundtrip():
    """Test that round trips work correctly."""
    paulis = QubitSparsePauliList.from_list(["IIIXX", "IZIYI"])

    encoded = QubitSparsePauliListModel.from_qubit_sparse_pauli_list(paulis)
    paulis_out = encoded.to_qubit_sparse_pauli_list()

    assert paulis == paulis_out
