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

"""QubitSparsePauliListModel"""

from pydantic import BaseModel, Field
from qiskit.quantum_info import QubitSparsePauliList


class QubitSparsePauliListModel(BaseModel):
    """Encoding of a qubit sparse Pauli list."""

    sparse_terms: list[tuple[str, list[int]]]
    """The Pauli terms in the sparse form ``(pauli_string, qubits)``."""

    num_qubits: int = Field(ge=0)
    """The total number of qubits the list applies to."""

    @classmethod
    def from_qubit_sparse_pauli_list(
        cls, qubit_sparse_pauli_list: QubitSparsePauliList
    ) -> "QubitSparsePauliListModel":
        """Encode a qubit sparse Pauli list into this model."""
        return cls(
            sparse_terms=qubit_sparse_pauli_list.to_sparse_list(),
            num_qubits=qubit_sparse_pauli_list.num_qubits,
        )

    def to_qubit_sparse_pauli_list(self) -> QubitSparsePauliList:
        """Decode this model into a qubit sparse Pauli list."""
        return QubitSparsePauliList.from_sparse_list(self.sparse_terms, self.num_qubits)
