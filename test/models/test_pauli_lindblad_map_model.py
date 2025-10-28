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

from qiskit.quantum_info import PauliLindbladMap

from ibm_quantum_schemas.models.pauli_lindblad_map_model import PauliLindbladMapModel


def test_roundtrip():
    """Test that round trips work correctly."""
    channel = PauliLindbladMap.from_list([("IIIXX", 0.1), ("IZIYI", -0.2)])

    encoded = PauliLindbladMapModel.from_pauli_lindblad_map(channel)
    channel_out = encoded.to_pauli_lindblad_map()

    assert channel == channel_out
