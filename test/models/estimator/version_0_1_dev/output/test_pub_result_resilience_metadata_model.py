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

"""Validation tests for pub_result_resilience_metadata_model.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.models.estimator.version_0_1_dev.output.pub_result_resilience_metadata_model import (
    PubResultResilienceMetadataModel,
)
from ibm_quantum_schemas.models.estimator.version_0_1_dev.output.pec_metadata_model import (
    PecMetadataModel,
)
from ibm_quantum_schemas.models.estimator.version_0_1_dev.output.layer_noise_metadata_model import (
    LayerNoiseMetadataModel,
)
from ibm_quantum_schemas.models.estimator.version_0_1_dev.output.pub_result_zne_metadata_model import (
    PubResultZneMetadataModel,
)


class TestPubResultResilienceMetadataModelValidation:
    """Test PubResultResilienceMetadataModel validation."""

    def test_valid_empty_metadata(self):
        """Test that empty metadata is valid."""
        model = PubResultResilienceMetadataModel.model_validate({})
        assert model.pec is None
        assert model.layer_noise is None
        assert model.zne is None

    def test_valid_with_pec_metadata(self):
        """Test that metadata with pec is valid."""
        pec_data = PecMetadataModel.model_validate({
            "num_randomizations_scaling": 1.5
        })
        data = {"pec": pec_data}
        model = PubResultResilienceMetadataModel.model_validate(data)
        assert model.pec is not None
        assert model.pec.num_randomizations_scaling == 1.5

    def test_pec_none(self):
        """Test that pec can be None."""
        data = {"pec": None}
        model = PubResultResilienceMetadataModel.model_validate(data)
        assert model.pec is None

    def test_valid_with_layer_noise_metadata(self):
        """Test that metadata with layer_noise is valid."""
        layer_noise_data = LayerNoiseMetadataModel.model_validate({
            "noise_overhead": 2.5,
            "total_mitigated_layers": 10,
        })
        data = {"layer_noise": layer_noise_data}
        model = PubResultResilienceMetadataModel.model_validate(data)
        assert model.layer_noise is not None
        assert model.layer_noise.noise_overhead == 2.5

    def test_layer_noise_none(self):
        """Test that layer_noise can be None."""
        data = {"layer_noise": None}
        model = PubResultResilienceMetadataModel.model_validate(data)
        assert model.layer_noise is None

    def test_valid_with_zne_metadata(self):
        """Test that metadata with zne is valid."""
        zne_data = PubResultZneMetadataModel.model_validate({
            "extrapolator": "exponential"
        })
        data = {"zne": zne_data}
        model = PubResultResilienceMetadataModel.model_validate(data)
        assert model.zne is not None
        assert model.zne.extrapolator == "exponential"

    def test_zne_none(self):
        """Test that zne can be None."""
        data = {"zne": None}
        model = PubResultResilienceMetadataModel.model_validate(data)
        assert model.zne is None

    def test_all_fields_together(self):
        """Test that all fields can be set together."""
        pec_data = PecMetadataModel.model_validate({
            "num_randomizations_scaling": 1.5
        })
        layer_noise_data = LayerNoiseMetadataModel.model_validate({
            "noise_overhead": 2.5,
            "total_mitigated_layers": 10,
            "unique_mitigated_layers": 5,
        })
        zne_data = PubResultZneMetadataModel.model_validate({
            "extrapolator": ["exponential", "linear"]
        })
        data = {
            "pec": pec_data,
            "layer_noise": layer_noise_data,
            "zne": zne_data,
        }
        model = PubResultResilienceMetadataModel.model_validate(data)
        assert model.pec is not None
        assert model.layer_noise is not None
        assert model.zne is not None

    def test_valid_with_layer_noise_infinity(self):
        """Test that layer_noise with infinity noise_overhead is valid."""
        layer_noise_data = LayerNoiseMetadataModel.model_validate({
            "noise_overhead": "infinity",
            "total_mitigated_layers": 5,
        })
        data = {"layer_noise": layer_noise_data}
        model = PubResultResilienceMetadataModel.model_validate(data)
        assert model.layer_noise.noise_overhead == "infinity"

    def test_valid_with_zne_list_extrapolator(self):
        """Test that zne with list extrapolator is valid."""
        zne_data = PubResultZneMetadataModel.model_validate({
            "extrapolator": ["exponential", "linear", "fallback"]
        })
        data = {"zne": zne_data}
        model = PubResultResilienceMetadataModel.model_validate(data)
        assert len(model.zne.extrapolator) == 3

    def test_extra_fields_forbidden(self):
        """Test that extra fields are forbidden."""
        data = {"extra_field": "not allowed"}
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            PubResultResilienceMetadataModel.model_validate(data)

    def test_serialization(self):
        """Test that serialization works correctly."""
        pec_data = PecMetadataModel.model_validate({
            "num_randomizations_scaling": 2.0
        })
        layer_noise_data = LayerNoiseMetadataModel.model_validate({
            "noise_overhead": 3.0,
            "total_mitigated_layers": 15,
        })
        zne_data = PubResultZneMetadataModel.model_validate({
            "extrapolator": "linear"
        })
        data = {
            "pec": pec_data,
            "layer_noise": layer_noise_data,
            "zne": zne_data,
        }
        model = PubResultResilienceMetadataModel.model_validate(data)
        serialized = model.model_dump()
        assert serialized["pec"] is not None
        assert serialized["layer_noise"] is not None
        assert serialized["zne"] is not None

    def test_serialization_with_none_values(self):
        """Test that serialization works with None values."""
        model = PubResultResilienceMetadataModel.model_validate({})
        serialized = model.model_dump()
        assert serialized["pec"] is None
        assert serialized["layer_noise"] is None
        assert serialized["zne"] is None

# Made with Bob
