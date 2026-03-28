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

"""Validation tests for layer_noise_metadata_model.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.estimator.version_0_1.layer_noise_metadata import (
    LayerNoiseMetadataModel,
)


class TestLayerNoiseMetadataModelValidation:
    """Test LayerNoiseMetadataModel validation."""

    def test_valid_empty_metadata(self):
        """Test that empty metadata is valid."""
        model = LayerNoiseMetadataModel.model_validate({})
        assert model.noise_overhead is None
        assert model.total_mitigated_layers is None
        assert model.unique_mitigated_layers is None
        assert model.unique_mitigated_layers_noise_overhead is None

    def test_valid_with_noise_overhead_float(self):
        """Test that metadata with float noise_overhead is valid."""
        data = {"noise_overhead": 1.5}
        model = LayerNoiseMetadataModel.model_validate(data)
        assert model.noise_overhead == 1.5

    def test_valid_with_noise_overhead_infinity(self):
        """Test that metadata with 'infinity' noise_overhead is valid."""
        data = {"noise_overhead": "infinity"}
        model = LayerNoiseMetadataModel.model_validate(data)
        assert model.noise_overhead == "infinity"

    def test_noise_overhead_zero(self):
        """Test that noise_overhead can be zero."""
        data = {"noise_overhead": 0.0}
        model = LayerNoiseMetadataModel.model_validate(data)
        assert model.noise_overhead == 0.0

    def test_noise_overhead_positive(self):
        """Test that noise_overhead accepts positive values."""
        data = {"noise_overhead": 2.5}
        model = LayerNoiseMetadataModel.model_validate(data)
        assert model.noise_overhead == 2.5

    def test_noise_overhead_negative(self):
        """Test that noise_overhead accepts negative values."""
        data = {"noise_overhead": -1.0}
        model = LayerNoiseMetadataModel.model_validate(data)
        assert model.noise_overhead == -1.0

    def test_noise_overhead_none(self):
        """Test that noise_overhead can be None."""
        data = {"noise_overhead": None}
        model = LayerNoiseMetadataModel.model_validate(data)
        assert model.noise_overhead is None

    def test_invalid_noise_overhead_string(self):
        """Test that invalid string values are rejected for noise_overhead."""
        data = {"noise_overhead": "invalid"}
        with pytest.raises(ValidationError):
            LayerNoiseMetadataModel.model_validate(data)

    def test_valid_with_total_mitigated_layers(self):
        """Test that metadata with total_mitigated_layers is valid."""
        data = {"total_mitigated_layers": 10}
        model = LayerNoiseMetadataModel.model_validate(data)
        assert model.total_mitigated_layers == 10

    def test_total_mitigated_layers_zero(self):
        """Test that total_mitigated_layers can be zero."""
        data = {"total_mitigated_layers": 0}
        model = LayerNoiseMetadataModel.model_validate(data)
        assert model.total_mitigated_layers == 0

    def test_total_mitigated_layers_negative_rejected(self):
        """Test that negative total_mitigated_layers is rejected."""
        data = {"total_mitigated_layers": -5}
        with pytest.raises(ValidationError):
            LayerNoiseMetadataModel.model_validate(data)

    def test_total_mitigated_layers_none(self):
        """Test that total_mitigated_layers can be None."""
        data = {"total_mitigated_layers": None}
        model = LayerNoiseMetadataModel.model_validate(data)
        assert model.total_mitigated_layers is None

    def test_valid_with_unique_mitigated_layers(self):
        """Test that metadata with unique_mitigated_layers is valid."""
        data = {"unique_mitigated_layers": 5}
        model = LayerNoiseMetadataModel.model_validate(data)
        assert model.unique_mitigated_layers == 5

    def test_unique_mitigated_layers_zero(self):
        """Test that unique_mitigated_layers can be zero."""
        data = {"unique_mitigated_layers": 0}
        model = LayerNoiseMetadataModel.model_validate(data)
        assert model.unique_mitigated_layers == 0

    def test_unique_mitigated_layers_negative_rejected(self):
        """Test that negative unique_mitigated_layers is rejected."""
        data = {"unique_mitigated_layers": -3}
        with pytest.raises(ValidationError):
            LayerNoiseMetadataModel.model_validate(data)

    def test_unique_mitigated_layers_none(self):
        """Test that unique_mitigated_layers can be None."""
        data = {"unique_mitigated_layers": None}
        model = LayerNoiseMetadataModel.model_validate(data)
        assert model.unique_mitigated_layers is None

    def test_valid_with_unique_mitigated_layers_noise_overhead(self):
        """Test that metadata with unique_mitigated_layers_noise_overhead is valid."""
        data = {"unique_mitigated_layers_noise_overhead": [1.5, 2.0, 3.5]}
        model = LayerNoiseMetadataModel.model_validate(data)
        assert model.unique_mitigated_layers_noise_overhead == [1.5, 2.0, 3.5]

    def test_unique_mitigated_layers_noise_overhead_with_infinity(self):
        """Test that unique_mitigated_layers_noise_overhead accepts 'infinity'."""
        data = {"unique_mitigated_layers_noise_overhead": [1.5, "infinity", 2.0]}
        model = LayerNoiseMetadataModel.model_validate(data)
        assert model.unique_mitigated_layers_noise_overhead == [1.5, "infinity", 2.0]

    def test_unique_mitigated_layers_noise_overhead_empty_list(self):
        """Test that unique_mitigated_layers_noise_overhead accepts empty list."""
        data = {"unique_mitigated_layers_noise_overhead": []}
        model = LayerNoiseMetadataModel.model_validate(data)
        assert model.unique_mitigated_layers_noise_overhead == []

    def test_unique_mitigated_layers_noise_overhead_none(self):
        """Test that unique_mitigated_layers_noise_overhead can be None."""
        data = {"unique_mitigated_layers_noise_overhead": None}
        model = LayerNoiseMetadataModel.model_validate(data)
        assert model.unique_mitigated_layers_noise_overhead is None

    def test_all_fields_together(self):
        """Test that all fields can be set together."""
        data = {
            "noise_overhead": 2.5,
            "total_mitigated_layers": 10,
            "unique_mitigated_layers": 5,
            "unique_mitigated_layers_noise_overhead": [1.5, 2.0, "infinity"],
        }
        model = LayerNoiseMetadataModel.model_validate(data)
        assert model.noise_overhead == 2.5
        assert model.total_mitigated_layers == 10
        assert model.unique_mitigated_layers == 5
        assert model.unique_mitigated_layers_noise_overhead == [1.5, 2.0, "infinity"]

    def test_serialization(self):
        """Test that serialization works correctly."""
        data = {
            "noise_overhead": 2.5,
            "total_mitigated_layers": 10,
            "unique_mitigated_layers": 5,
            "unique_mitigated_layers_noise_overhead": [1.5, 2.0, "infinity"],
        }
        model = LayerNoiseMetadataModel.model_validate(data)
        serialized = model.model_dump()
        assert serialized["noise_overhead"] == 2.5
        assert serialized["total_mitigated_layers"] == 10
        assert serialized["unique_mitigated_layers"] == 5
        assert serialized["unique_mitigated_layers_noise_overhead"] == [1.5, 2.0, "infinity"]
