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

"""Validation tests for observables_array_model.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.models.estimator.version_0_1_dev.observables_array_model import (
    ObservableModel,
    ObservablesArrayModel,
)


class TestObservableModelValidation:
    """Test ObservableModel validation."""

    def test_valid_single_observable(self):
        """Test that a valid single observable is accepted."""
        obs = ObservableModel.model_validate({"XX": 0.5, "YY": 0.5})
        assert obs.root == {"XX": 0.5, "YY": 0.5}

    def test_valid_empty_observable(self):
        """Test that an empty observable is accepted."""
        obs = ObservableModel.model_validate({})
        assert obs.root == {}

    def test_valid_single_pauli_string(self):
        """Test that a single Pauli string is accepted."""
        obs = ObservableModel.model_validate({"IXYZ": 1.0})
        assert obs.root == {"IXYZ": 1.0}

    def test_valid_all_identity(self):
        """Test that all identity Pauli string is accepted."""
        obs = ObservableModel.model_validate({"IIII": 1.0})
        assert obs.root == {"IIII": 1.0}

    def test_valid_empty_string(self):
        """Test that empty string Pauli is accepted."""
        obs = ObservableModel.model_validate({"": 1.0})
        assert obs.root == {"": 1.0}

    def test_invalid_pauli_characters(self):
        """Test that invalid Pauli characters are rejected."""
        with pytest.raises(ValidationError, match=r"invalid characters"):
            ObservableModel.model_validate({"XA": 1.0})

    def test_invalid_lowercase_pauli(self):
        """Test that lowercase Pauli characters are rejected."""
        with pytest.raises(ValidationError, match=r"invalid characters"):
            ObservableModel.model_validate({"xx": 1.0})

    def test_invalid_numeric_characters(self):
        """Test that numeric characters are rejected."""
        with pytest.raises(ValidationError, match=r"invalid characters"):
            ObservableModel.model_validate({"X1": 1.0})

    def test_different_length_pauli_strings(self):
        """Test that Pauli strings of different lengths are rejected."""
        with pytest.raises(ValidationError, match=r"same length"):
            ObservableModel.model_validate({"XX": 1.0, "YYY": 2.0})

    def test_multiple_different_lengths(self):
        """Test that multiple different lengths are rejected."""
        with pytest.raises(ValidationError, match=r"same length"):
            ObservableModel.model_validate({"X": 1.0, "YY": 2.0, "ZZZ": 3.0})

    def test_negative_coefficients(self):
        """Test that negative coefficients are accepted."""
        obs = ObservableModel.model_validate({"XX": -0.5, "YY": 0.5})
        assert obs.root == {"XX": -0.5, "YY": 0.5}

    def test_zero_coefficients(self):
        """Test that zero coefficients are accepted."""
        obs = ObservableModel.model_validate({"XX": 0.0, "YY": 1.0})
        assert obs.root == {"XX": 0.0, "YY": 1.0}


class TestObservablesArrayModelValidation:
    """Test ObservablesArrayModel validation."""

    def test_single_observable(self):
        """Test that a single observable is accepted."""
        obs_array = ObservablesArrayModel.model_validate({"XX": 0.5, "YY": 0.5})
        assert isinstance(obs_array.root, ObservableModel)
        assert obs_array.root.root == {"XX": 0.5, "YY": 0.5}

    def test_list_of_observables_same_length(self):
        """Test that a list of observables with same length is accepted."""
        obs_array = ObservablesArrayModel.model_validate([
            {"XI": 1.0, "YZ": 2.0},
            {"ZZ": 3.0, "XY": 4.0}
        ])
        assert obs_array.root == [
            {"XI": 1.0, "YZ": 2.0},
            {"ZZ": 3.0, "XY": 4.0}
        ]

    def test_list_of_observables_different_lengths(self):
        """Test that a list of observables with different lengths is rejected."""
        with pytest.raises(ValidationError, match=r"same length"):
            ObservablesArrayModel.model_validate([
                {"XI": 1.0, "YZ": 2.0},  # Length 2
                {"ZZZ": 3.0, "XYZ": 4.0}  # Length 3
            ])

    def test_list_with_single_observable(self):
        """Test that a list with a single observable is accepted."""
        obs_array = ObservablesArrayModel.model_validate([{"XX": 1.0}])
        assert obs_array.root == [{"XX": 1.0}]

    def test_empty_list(self):
        """Test that an empty list is accepted."""
        obs_array = ObservablesArrayModel.model_validate([])
        assert obs_array.root == []

    def test_list_with_empty_observables(self):
        """Test that a list with empty observables is accepted."""
        obs_array = ObservablesArrayModel.model_validate([{}, {}])
        assert obs_array.root == [{}, {}]

    def test_mixed_empty_and_non_empty_observables_same_length(self):
        """Test that mixed empty and non-empty observables with same length is accepted."""
        obs_array = ObservablesArrayModel.model_validate([
            {},
            {"XX": 1.0, "YY": 2.0}
        ])
        assert obs_array.root == [
            {},
            {"XX": 1.0, "YY": 2.0}
        ]

    def test_complex_valid_case(self):
        """Test a complex valid case with multiple observables."""
        obs_array = ObservablesArrayModel.model_validate([
            {"IXYZ": 1.0, "ZZII": 2.0},
            {"XXXX": 3.0},
            {"YYYY": 4.0, "ZZZZ": 5.0, "IIII": 6.0}
        ])
        assert obs_array.root == [
            {"IXYZ": 1.0, "ZZII": 2.0},
            {"XXXX": 3.0},
            {"YYYY": 4.0, "ZZZZ": 5.0, "IIII": 6.0}
        ]

    def test_complex_invalid_case(self):
        """Test a complex invalid case with observables of different lengths."""
        with pytest.raises(ValidationError, match=r"same length"):
            ObservablesArrayModel.model_validate([
                {"IXYZ": 1.0, "ZZII": 2.0},  # Length 4
                {"XXX": 3.0},  # Length 3
                {"YYYY": 4.0, "ZZZZ": 5.0}  # Length 4
            ])

    def test_single_observable_with_invalid_pauli(self):
        """Test that single observable with invalid Pauli is rejected."""
        with pytest.raises(ValidationError, match=r"invalid characters"):
            ObservablesArrayModel.model_validate({"XA": 1.0})

    def test_list_with_invalid_pauli_in_one_observable(self):
        """Test that list with invalid Pauli in one observable is rejected."""
        with pytest.raises(ValidationError, match=r"invalid characters"):
            ObservablesArrayModel.model_validate([
                {"XX": 1.0},
                {"YA": 2.0}  # Invalid
            ])

    def test_list_with_different_lengths_within_observable(self):
        """Test that list with different lengths within one observable is rejected."""
        with pytest.raises(ValidationError, match=r"same length"):
            ObservablesArrayModel.model_validate([
                {"XX": 1.0, "YYY": 2.0},  # Different lengths within same observable
                {"ZZ": 3.0}
            ])
