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

"""Observables Array Model"""

from typing import Annotated

from pydantic import AfterValidator


def validate_pauli_string(value: str) -> str:
    """Validate that a string contains only Pauli characters (I, X, Y, Z)."""
    valid_chars = set("IXYZ")
    if not all(char in valid_chars for char in value):
        invalid_chars = set(value) - valid_chars
        raise ValueError(
            f"Pauli string contains invalid characters: {invalid_chars}. "
            "Only I, X, Y, Z are allowed."
        )
    
    return value


PauliString = Annotated[str, AfterValidator(validate_pauli_string)]
"""A string representing a Pauli operator, where each character is one of I, X, Y, or Z.

An empty string is also allowed.

Examples:
    - "IXYZ"
    - "ZZII"
    - "XYZ"
    - ""
"""