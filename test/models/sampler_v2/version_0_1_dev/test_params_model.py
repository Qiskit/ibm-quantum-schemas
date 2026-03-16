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

"""Validation tests for params_model.py classes."""

from ibm_quantum_schemas.models.sampler_v2.version_0_1_dev.params_model import ParamsModel


class TestParamsModelValidation:
    """Test ParamsModel validation."""

    def test_valid_params_with_defaults(self, valid_sampler_pub):
        """Test that valid params with defaults are accepted."""
        params = {"pubs": [valid_sampler_pub]}
        model = ParamsModel.model_validate(params)

        assert len(model.pubs) == 1
        assert model.pubs[0].root[0].type_ == valid_sampler_pub[0]["__type__"]
        assert model.pubs[0].root[2] == valid_sampler_pub[2]
        assert model.support_qiskit is True
        assert model.version == 2
        assert model.options.default_shots == 4096

    def test_valid_params_with_custom_options(self, valid_sampler_pub):
        """Test that params with custom options are accepted."""
        params = {
            "pubs": [valid_sampler_pub],
            "options": {
                "default_shots": 2000,
                "dynamical_decoupling": {"enable": True},
            },
        }
        model = ParamsModel.model_validate(params)

        assert len(model.pubs) == 1
        assert model.options.default_shots == 2000
        assert model.options.dynamical_decoupling.enable is True
