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

"""Shared utility functions for model tests."""

import zlib
from io import BytesIO

import pybase64
from qiskit.circuit import QuantumCircuit
from qiskit.qpy import dump as qpy_dump


@pytest.fixture
def compressed_qpy_circuit_v13() -> str:
    """Fixture to create a base64-encoded, zlib-compressed QPY circuit (version 13).

    Returns:
        Base64-encoded string of the compressed QPY circuit data.
    """
    buffer = BytesIO()
    qpy_dump(circuit, buffer, version=13)
    qpy_data = buffer.getvalue()
    compressed = zlib.compress(qpy_data)
    encoded = pybase64.b64encode(compressed).decode("utf-8")

    return encoded


@pytest.fixture
def valid_typed_qpy_circuit_dict_v13(compressed_qpy_circuit_v13) -> dict:
    """Fixture to create a valid TypedQpyCircuitModel dict with QPY v13.

    Args:
        compressed_qpy_circuit_v13: Base64-encoded compressed QPY circuit (version 13).

    Returns:
        Dictionary with __type__ and __value__ fields for TypedQpyCircuitModel.
    """
    return {"__type__": "QuantumCircuit", "__value__": compressed_qpy_circuit_v13}
