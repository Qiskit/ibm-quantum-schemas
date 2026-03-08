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

"""Validation tests for primitive_result_resilience_metadata_model.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.models.estimator.version_0_1_dev.output.layer_noise_model_metadata_model import (  # noqa: E501
    LayerNoiseModelMetadataWrapperModel,
)
from ibm_quantum_schemas.models.estimator.version_0_1_dev.output.primitive_result_resilience_metadata_model import (  # noqa: E501
    PrimitiveResultResilienceMetadataModel,
)
from ibm_quantum_schemas.models.estimator.version_0_1_dev.output.primitive_result_zne_metadata_model import (  # noqa: E501
    PrimitiveResultZneMetadataModel,
)


class TestPrimitiveResultResilienceMetadataModelValidation:
    """Test PrimitiveResultResilienceMetadataModel validation."""

    def test_valid_empty_metadata(self):
        """Test that empty metadata is valid."""
        model = PrimitiveResultResilienceMetadataModel.model_validate({})
        assert model.measure_mitigation is None
        assert model.zne_mitigation is None
        assert model.pec_mitigation is None
        assert model.zne is None
        assert model.layer_noise_model is None

    def test_valid_with_measure_mitigation(self):
        """Test that metadata with measure_mitigation is valid."""
        data = {"measure_mitigation": True}
        model = PrimitiveResultResilienceMetadataModel.model_validate(data)
        assert model.measure_mitigation is True

    def test_measure_mitigation_false(self):
        """Test that measure_mitigation can be False."""
        data = {"measure_mitigation": False}
        model = PrimitiveResultResilienceMetadataModel.model_validate(data)
        assert model.measure_mitigation is False

    def test_measure_mitigation_none(self):
        """Test that measure_mitigation can be None."""
        data = {"measure_mitigation": None}
        model = PrimitiveResultResilienceMetadataModel.model_validate(data)
        assert model.measure_mitigation is None

    def test_valid_with_zne_mitigation(self):
        """Test that metadata with zne_mitigation is valid."""
        data = {"zne_mitigation": True}
        model = PrimitiveResultResilienceMetadataModel.model_validate(data)
        assert model.zne_mitigation is True

    def test_zne_mitigation_false(self):
        """Test that zne_mitigation can be False."""
        data = {"zne_mitigation": False}
        model = PrimitiveResultResilienceMetadataModel.model_validate(data)
        assert model.zne_mitigation is False

    def test_zne_mitigation_none(self):
        """Test that zne_mitigation can be None."""
        data = {"zne_mitigation": None}
        model = PrimitiveResultResilienceMetadataModel.model_validate(data)
        assert model.zne_mitigation is None

    def test_valid_with_pec_mitigation(self):
        """Test that metadata with pec_mitigation is valid."""
        data = {"pec_mitigation": True}
        model = PrimitiveResultResilienceMetadataModel.model_validate(data)
        assert model.pec_mitigation is True

    def test_pec_mitigation_false(self):
        """Test that pec_mitigation can be False."""
        data = {"pec_mitigation": False}
        model = PrimitiveResultResilienceMetadataModel.model_validate(data)
        assert model.pec_mitigation is False

    def test_pec_mitigation_none(self):
        """Test that pec_mitigation can be None."""
        data = {"pec_mitigation": None}
        model = PrimitiveResultResilienceMetadataModel.model_validate(data)
        assert model.pec_mitigation is None

    def test_valid_with_zne_metadata(self):
        """Test that metadata with zne metadata is valid."""
        zne_data = PrimitiveResultZneMetadataModel.model_validate(
            {
                "noise_factors": [1.0, 2.0],
                "extrapolator": "exponential",
            }
        )
        data = {"zne": zne_data}
        model = PrimitiveResultResilienceMetadataModel.model_validate(data)
        assert model.zne == zne_data
        assert model.zne.noise_factors == [1.0, 2.0]
        assert model.zne.extrapolator == "exponential"

    def test_zne_none(self):
        """Test that zne can be None."""
        data = {"zne": None}
        model = PrimitiveResultResilienceMetadataModel.model_validate(data)
        assert model.zne is None

    def test_valid_with_layer_noise_model(self, valid_layer_noise_wrapper):
        """Test that metadata with layer_noise_model is valid."""
        data = {"layer_noise_model": [valid_layer_noise_wrapper]}
        model = PrimitiveResultResilienceMetadataModel.model_validate(data)
        assert len(model.layer_noise_model) == 1
        expected_wrapper = LayerNoiseModelMetadataWrapperModel.model_validate(
            valid_layer_noise_wrapper
        )
        assert model.layer_noise_model[0] == expected_wrapper

    def test_layer_noise_model_empty_list(self):
        """Test that layer_noise_model accepts empty list."""
        data = {"layer_noise_model": []}
        model = PrimitiveResultResilienceMetadataModel.model_validate(data)
        assert model.layer_noise_model == []

    def test_layer_noise_model_multiple(self, valid_layer_noise_wrapper):
        """Test that layer_noise_model accepts multiple items."""
        data = {"layer_noise_model": [valid_layer_noise_wrapper, valid_layer_noise_wrapper]}
        model = PrimitiveResultResilienceMetadataModel.model_validate(data)
        assert len(model.layer_noise_model) == 2

    def test_layer_noise_model_none(self):
        """Test that layer_noise_model can be None."""
        data = {"layer_noise_model": None}
        model = PrimitiveResultResilienceMetadataModel.model_validate(data)
        assert model.layer_noise_model is None

    def test_all_fields_together(self, valid_layer_noise_wrapper):
        """Test that all fields can be set together."""
        zne_data = PrimitiveResultZneMetadataModel.model_validate(
            {
                "noise_factors": [1.0, 2.0],
            }
        )
        data = {
            "measure_mitigation": True,
            "zne_mitigation": True,
            "pec_mitigation": False,
            "zne": zne_data,
            "layer_noise_model": [valid_layer_noise_wrapper],
        }
        model = PrimitiveResultResilienceMetadataModel.model_validate(data)
        assert model.measure_mitigation is True
        assert model.zne_mitigation is True
        assert model.pec_mitigation is False
        assert model.zne == zne_data
        assert len(model.layer_noise_model) == 1
        expected_wrapper = LayerNoiseModelMetadataWrapperModel.model_validate(
            valid_layer_noise_wrapper
        )
        assert model.layer_noise_model[0] == expected_wrapper

    def test_extra_fields_forbidden(self):
        """Test that extra fields are forbidden."""
        data = {"extra_field": "not allowed"}
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            PrimitiveResultResilienceMetadataModel.model_validate(data)

    def test_serialization(self, valid_layer_noise_wrapper):
        """Test that serialization works correctly."""
        zne_data = PrimitiveResultZneMetadataModel.model_validate(
            {
                "noise_factors": [1.0, 2.0],
                "extrapolator": "linear",
            }
        )
        data = {
            "measure_mitigation": True,
            "zne_mitigation": False,
            "pec_mitigation": True,
            "zne": zne_data,
            "layer_noise_model": [valid_layer_noise_wrapper],
        }
        model = PrimitiveResultResilienceMetadataModel.model_validate(data)
        serialized = model.model_dump()
        assert serialized["measure_mitigation"] is True
        assert serialized["zne_mitigation"] is False
        assert serialized["pec_mitigation"] is True
        assert "zne" in serialized
        assert serialized["zne"]["noise_factors"] == [1.0, 2.0]
        assert serialized["zne"]["extrapolator"] == "linear"
        assert "layer_noise_model" in serialized
        assert len(serialized["layer_noise_model"]) == 1
