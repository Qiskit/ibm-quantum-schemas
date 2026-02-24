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

"""Validation tests for models.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.models.estimator.version_0_1_dev.models import ParamsModel


class TestParamsModelValidation:
    """Test ParamsModel validation."""

    def test_valid_params_model(self, valid_estimator_pub):
        """Test that valid params are accepted."""
        params = {
            "pubs": [valid_estimator_pub],
            "options": {},
        }
        model = ParamsModel.model_validate(params)
        assert model.schema_version == "v0.1"
        assert model.pubs == [valid_estimator_pub]
        assert model.support_qiskit is True
        assert model.version == 2
        assert model.resilience_level == 1

    def test_missing_pubs_field(self):
        """Test that missing pubs field is rejected."""
        params = {"options": {}}
        with pytest.raises(ValidationError, match="Field required"):
            ParamsModel.model_validate(params)

    def test_empty_pubs_list(self):
        """Test that empty pubs list is accepted."""
        params = {"pubs": []}
        model = ParamsModel.model_validate(params)
        assert model.pubs == []

    def test_multiple_pubs(self, valid_estimator_pub):
        """Test that multiple pubs are accepted."""
        params = {
            "pubs": [
                valid_estimator_pub,
                valid_estimator_pub,
                valid_estimator_pub,
            ],
        }
        model = ParamsModel.model_validate(params)
        assert model.pubs == [valid_estimator_pub, valid_estimator_pub, valid_estimator_pub]

    def test_support_qiskit_must_be_true(self, valid_estimator_pub):
        """Test that support_qiskit must be True."""
        params = {
            "pubs": [valid_estimator_pub],
            "support_qiskit": False,
        }
        with pytest.raises(ValidationError, match="Input should be True"):
            ParamsModel.model_validate(params)

    def test_version_must_be_2(self, valid_estimator_pub):
        """Test that version must be 2."""
        params = {
            "pubs": [valid_estimator_pub],
            "version": 1,
        }
        with pytest.raises(ValidationError, match="Input should be 2"):
            ParamsModel.model_validate(params)

    def test_resilience_level_default(self, valid_estimator_pub):
        """Test that resilience_level has default value of 1."""
        params = {"pubs": [valid_estimator_pub]}
        model = ParamsModel.model_validate(params)
        assert model.resilience_level == 1

    def test_resilience_level_valid_values(self, valid_estimator_pub):
        """Test that valid resilience_level values are accepted."""
        for level in [0, 1, 2]:
            params = {
                "pubs": [valid_estimator_pub],
                "resilience_level": level,
            }
            model = ParamsModel.model_validate(params)
            assert model.resilience_level == level

    def test_resilience_level_negative(self, valid_estimator_pub):
        """Test that negative resilience_level is rejected."""
        params = {
            "pubs": [valid_estimator_pub],
            "resilience_level": -1,
        }
        with pytest.raises(ValidationError, match="greater than or equal to 0"):
            ParamsModel.model_validate(params)

    def test_resilience_level_too_high(self, valid_estimator_pub):
        """Test that resilience_level > 2 is rejected."""
        params = {
            "pubs": [valid_estimator_pub],
            "resilience_level": 3,
        }
        with pytest.raises(ValidationError, match="less than or equal to 2"):
            ParamsModel.model_validate(params)

    def test_options_default_factory(self, valid_estimator_pub):
        """Test that options has default factory."""
        params = {"pubs": [valid_estimator_pub]}
        model = ParamsModel.model_validate(params)
        assert model.options.default_precision == 0.015625

    def test_custom_options(self, valid_estimator_pub):
        """Test that custom options are accepted."""
        params = {
            "pubs": [valid_estimator_pub],
            "options": {
                "default_precision": 0.01,
                "default_shots": 1000,
            },
        }
        model = ParamsModel.model_validate(params)
        assert model.options.default_precision == 0.01
        assert model.options.default_shots == 1000

    def test_extra_fields_forbidden(self, valid_estimator_pub):
        """Test that extra fields are forbidden."""
        params = {
            "pubs": [valid_estimator_pub],
            "extra_field": "not allowed",
        }
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            ParamsModel.model_validate(params)
