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

"""Validation tests for resilience_options_model.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.models.estimator.version_0_1_dev.resilience_options_model import (
    ResilienceOptionsModel,
)


class TestResilienceOptionsModelValidation:
    """Test ResilienceOptionsModel validation."""

    def test_valid_resilience_options_with_defaults(self):
        """Test that resilience options with default values are accepted."""
        model = ResilienceOptionsModel.model_validate({})
        assert model.measure_mitigation is True
        assert model.zne_mitigation is False
        assert model.pec_mitigation is False
        assert model.measure_noise_learning is not None
        assert model.zne is not None
        assert model.pec is not None
        assert model.layer_noise_learning is not None
        assert model.layer_noise_model is None

    def test_valid_resilience_options_with_custom_values(self):
        """Test that custom resilience option values are accepted."""
        options = {
            "measure_mitigation": False,
            "zne_mitigation": True,
            "pec_mitigation": False,
        }
        model = ResilienceOptionsModel.model_validate(options)
        assert model.measure_mitigation is False
        assert model.zne_mitigation is True
        assert model.pec_mitigation is False

    def test_zne_and_pec_both_enabled_rejected(self):
        """Test that enabling both ZNE and PEC is rejected."""
        options = {
            "zne_mitigation": True,
            "pec_mitigation": True,
        }
        with pytest.raises(
            ValidationError,
            match="'pec_mitigation' and 'zne_mitigation' options cannot be simultaneously enabled",
        ):
            ResilienceOptionsModel.model_validate(options)

    def test_zne_enabled_pec_disabled(self):
        """Test that ZNE enabled with PEC disabled is accepted."""
        options = {
            "zne_mitigation": True,
            "pec_mitigation": False,
        }
        model = ResilienceOptionsModel.model_validate(options)
        assert model.zne_mitigation is True
        assert model.pec_mitigation is False

    def test_pec_enabled_zne_disabled(self):
        """Test that PEC enabled with ZNE disabled is accepted."""
        options = {
            "zne_mitigation": False,
            "pec_mitigation": True,
        }
        model = ResilienceOptionsModel.model_validate(options)
        assert model.zne_mitigation is False
        assert model.pec_mitigation is True

    def test_both_zne_and_pec_disabled(self):
        """Test that both ZNE and PEC disabled is accepted."""
        options = {
            "zne_mitigation": False,
            "pec_mitigation": False,
        }
        model = ResilienceOptionsModel.model_validate(options)
        assert model.zne_mitigation is False
        assert model.pec_mitigation is False

    def test_nested_measure_noise_learning_options(self):
        """Test that nested measure_noise_learning options are accepted."""
        options = {
            "measure_noise_learning": {
                "num_randomizations": 64,
                "shots_per_randomization": 256,
            }
        }
        model = ResilienceOptionsModel.model_validate(options)
        assert model.measure_noise_learning.num_randomizations == 64
        assert model.measure_noise_learning.shots_per_randomization == 256

    def test_nested_zne_options(self):
        """Test that nested zne options are accepted."""
        options = {
            "zne": {
                "noise_factors": [1, 3, 5],
                "extrapolator": "linear",
            }
        }
        model = ResilienceOptionsModel.model_validate(options)
        assert model.zne.noise_factors == [1, 3, 5]
        assert model.zne.extrapolator == "linear"

    def test_nested_pec_options(self):
        """Test that nested pec options are accepted."""
        options = {
            "pec": {
                "max_overhead": 100,
            }
        }
        model = ResilienceOptionsModel.model_validate(options)
        assert model.pec.max_overhead == 100

    def test_nested_layer_noise_learning_options(self):
        """Test that nested layer_noise_learning options are accepted."""
        options = {
            "layer_noise_learning": {
                "max_layers_to_learn": 5,
                "shots_per_randomization": 128,
            }
        }
        model = ResilienceOptionsModel.model_validate(options)
        assert model.layer_noise_learning.max_layers_to_learn == 5
        assert model.layer_noise_learning.shots_per_randomization == 128

    def test_layer_noise_model_with_sequence(self, valid_layer_noise_wrapper):
        """Test that layer_noise_model accepts a sequence of LayerNoiseWrapperModel."""
        options = {
            "layer_noise_model": [valid_layer_noise_wrapper, valid_layer_noise_wrapper]
        }
        model = ResilienceOptionsModel.model_validate(options)
        assert model.layer_noise_model is not None
        assert len(model.layer_noise_model) == 2

    def test_layer_noise_model_none(self):
        """Test that layer_noise_model can be None."""
        options = {"layer_noise_model": None}
        model = ResilienceOptionsModel.model_validate(options)
        assert model.layer_noise_model is None

    def test_extra_fields_forbidden(self):
        """Test that extra fields are forbidden."""
        options = {"extra_field": "not allowed"}
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            ResilienceOptionsModel.model_validate(options)

    def test_all_mitigation_disabled(self):
        """Test that all mitigation methods can be disabled."""
        options = {
            "measure_mitigation": False,
            "zne_mitigation": False,
            "pec_mitigation": False,
        }
        model = ResilienceOptionsModel.model_validate(options)
        assert model.measure_mitigation is False
        assert model.zne_mitigation is False
        assert model.pec_mitigation is False

    def test_measure_mitigation_with_zne(self):
        """Test that measure_mitigation can be enabled with ZNE."""
        options = {
            "measure_mitigation": True,
            "zne_mitigation": True,
            "pec_mitigation": False,
        }
        model = ResilienceOptionsModel.model_validate(options)
        assert model.measure_mitigation is True
        assert model.zne_mitigation is True
        assert model.pec_mitigation is False

    def test_measure_mitigation_with_pec(self):
        """Test that measure_mitigation can be enabled with PEC."""
        options = {
            "measure_mitigation": True,
            "zne_mitigation": False,
            "pec_mitigation": True,
        }
        model = ResilienceOptionsModel.model_validate(options)
        assert model.measure_mitigation is True
        assert model.zne_mitigation is False
        assert model.pec_mitigation is True

# Made with Bob
