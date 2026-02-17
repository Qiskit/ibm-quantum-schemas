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

from pydantic import AfterValidator, RootModel, model_validator

from ....aliases import Self


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


class ObservableModel(RootModel[dict[PauliString, float]]):
    """A mapping of Pauli strings to their coefficients.
    
    Represents a quantum observable as a linear combination of Pauli operators,
    where each Pauli string is mapped to its coefficient (weight).
    All Pauli strings must have the same length.
    
    Example: {"XX": 0.5, "YY": 0.5} represents 0.5*XX + 0.5*YY
    """
    
    root: dict[PauliString, float]
    
    @model_validator(mode="after")
    def validate_same_length(self) -> Self:
        """Validate that all Pauli strings have the same length."""
        if not self.root:
            return self
        
        lengths = {len(pauli_str) for pauli_str in self.root.keys()}
        if len(lengths) > 1:
            raise ValueError(
                f"All Pauli strings must have the same length. Found lengths: {sorted(lengths)}"
            )
        
        return self


class ObservablesArrayModel(RootModel[ObservableModel | list[ObservableModel]]):
    """Either a single observable or a list of observables.
    
    When a list of observables is provided, all observables must have the same length
    (i.e., all Pauli strings across all observables must have the same length).

    Examples:
        - Single observable: {"XX": 0.5, "YY": 0.5}
        - List of observables: [{"XX": 1.0}, {"YY": 1.0, "ZZ": 1.0}]
    """
    
    root: ObservableModel | list[ObservableModel]
    
    @model_validator(mode="after")
    def validate_all_observables_same_length(self) -> Self:
        """Validate that all observables in the array have the same length."""
        # If it's a single observable, no cross-observable validation needed
        if not isinstance(self.root, list):
            return self
        
        # If the list is empty or has only one observable, no validation needed
        if len(self.root) <= 1:
            return self
        
        # Collect all lengths from all observables
        all_lengths = set()
        for observable in self.root:
            if observable.root:  # Skip empty observables
                # Get the length of Pauli strings in this observable
                lengths = {len(pauli_str) for pauli_str in observable.root.keys()}
                all_lengths.update(lengths)
        
        # Check if all lengths are the same
        if len(all_lengths) > 1:
            raise ValueError(
                f"All observables in the array must have the same length. "
                f"Found Pauli string lengths: {sorted(all_lengths)}"
            )
        
        return self