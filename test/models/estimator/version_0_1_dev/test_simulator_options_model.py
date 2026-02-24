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

"""Validation tests for simulator_options_model.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.models.estimator.version_0_1_dev.simulator_options_model import (
    NoiseModel,
    SimulatorOptionsModel,
)


class TestNoiseModelValidation:
    """Test NoiseModel validation."""

    def test_valid_noise_model(self):
        """Test that a valid noise model is accepted."""
        noise_data = {
            "__type__": "NoiseModel",
            "__value__": {"errors": [], "basis_gates": ["cx", "id", "rz", "sx", "x"]},
        }
        model = NoiseModel.model_validate(noise_data)
        assert model.type_ == "NoiseModel"
        assert model.value_ == {"errors": [], "basis_gates": ["cx", "id", "rz", "sx", "x"]}

    def test_noise_model_default_type(self):
        """Test that type defaults to 'NoiseModel'."""
        noise_data = {"__value__": {"errors": []}}
        model = NoiseModel.model_validate(noise_data)
        assert model.type_ == "NoiseModel"

    def test_noise_model_empty_value(self):
        """Test that empty value dict is accepted."""
        noise_data = {"__type__": "NoiseModel", "__value__": {}}
        model = NoiseModel.model_validate(noise_data)
        assert model.value_ == {}

    def test_noise_model_missing_value_rejected(self):
        """Test that missing __value__ is rejected."""
        noise_data = {"__type__": "NoiseModel"}
        with pytest.raises(ValidationError, match="Field required"):
            NoiseModel.model_validate(noise_data)


class TestSimulatorOptionsModelValidation:
    """Test SimulatorOptionsModel validation."""

    def test_valid_options_with_defaults(self):
        """Test that simulator options with default values are accepted."""
        model = SimulatorOptionsModel.model_validate({})
        
        # Verify all default values
        assert model.noise_model is None
        assert model.seed_simulator is None
        assert model.coupling_map is None
        assert model.basis_gates is None

    def test_valid_options_with_custom_values(self):
        """Test that custom simulator option values are accepted."""
        options = {
            "seed_simulator": 42,
            "coupling_map": [[0, 1], [1, 2]],
            "basis_gates": ["cx", "id", "rz", "sx"],
        }
        model = SimulatorOptionsModel.model_validate(options)
        assert model.seed_simulator == 42
        assert model.coupling_map == [[0, 1], [1, 2]]
        assert model.basis_gates == ["cx", "id", "rz", "sx"]

    def test_noise_model_none(self):
        """Test that noise_model can be None."""
        options = {"noise_model": None}
        model = SimulatorOptionsModel.model_validate(options)
        assert model.noise_model is None

    def test_noise_model_with_data(self):
        """Test that noise_model with data is accepted."""
        options = {
            "noise_model": {
                "__type__": "NoiseModel",
                "__value__": {"errors": [], "basis_gates": ["cx", "id"]},
            }
        }
        model = SimulatorOptionsModel.model_validate(options)
        assert model.noise_model is not None
        assert model.noise_model.type_ == "NoiseModel"
        assert model.noise_model.value_["basis_gates"] == ["cx", "id"]

    def test_seed_simulator_none(self):
        """Test that seed_simulator can be None."""
        options = {"seed_simulator": None}
        model = SimulatorOptionsModel.model_validate(options)
        assert model.seed_simulator is None

    def test_seed_simulator_zero(self):
        """Test that seed_simulator can be zero."""
        options = {"seed_simulator": 0}
        model = SimulatorOptionsModel.model_validate(options)
        assert model.seed_simulator == 0

    def test_seed_simulator_positive(self):
        """Test that positive seed_simulator is accepted."""
        options = {"seed_simulator": 12345}
        model = SimulatorOptionsModel.model_validate(options)
        assert model.seed_simulator == 12345

    def test_seed_simulator_negative(self):
        """Test that negative seed_simulator is accepted."""
        # Note: Model doesn't enforce non-negative
        options = {"seed_simulator": -1}
        model = SimulatorOptionsModel.model_validate(options)
        assert model.seed_simulator == -1

    def test_coupling_map_none(self):
        """Test that coupling_map can be None."""
        options = {"coupling_map": None}
        model = SimulatorOptionsModel.model_validate(options)
        assert model.coupling_map is None

    def test_coupling_map_empty(self):
        """Test that empty coupling_map is accepted."""
        options = {"coupling_map": []}
        model = SimulatorOptionsModel.model_validate(options)
        assert model.coupling_map == []

    def test_coupling_map_single_edge(self):
        """Test that coupling_map with single edge is accepted."""
        options = {"coupling_map": [[0, 1]]}
        model = SimulatorOptionsModel.model_validate(options)
        assert model.coupling_map == [[0, 1]]

    def test_coupling_map_multiple_edges(self):
        """Test that coupling_map with multiple edges is accepted."""
        options = {"coupling_map": [[0, 1], [1, 2], [2, 3], [3, 0]]}
        model = SimulatorOptionsModel.model_validate(options)
        assert model.coupling_map == [[0, 1], [1, 2], [2, 3], [3, 0]]

    def test_coupling_map_invalid_length_rejected(self):
        """Test that coupling_map with invalid edge length is rejected."""
        options = {"coupling_map": [[0, 1, 2]]}
        with pytest.raises(ValidationError, match="List should have at most 2 items"):
            SimulatorOptionsModel.model_validate(options)

    def test_coupling_map_single_element_rejected(self):
        """Test that coupling_map with single element edges is rejected."""
        options = {"coupling_map": [[0]]}
        with pytest.raises(ValidationError, match="List should have at least 2 items"):
            SimulatorOptionsModel.model_validate(options)

    def test_basis_gates_none(self):
        """Test that basis_gates can be None."""
        options = {"basis_gates": None}
        model = SimulatorOptionsModel.model_validate(options)
        assert model.basis_gates is None

    def test_basis_gates_empty(self):
        """Test that empty basis_gates is accepted."""
        options = {"basis_gates": []}
        model = SimulatorOptionsModel.model_validate(options)
        assert model.basis_gates == []

    def test_basis_gates_single_gate(self):
        """Test that basis_gates with single gate is accepted."""
        options = {"basis_gates": ["cx"]}
        model = SimulatorOptionsModel.model_validate(options)
        assert model.basis_gates == ["cx"]

    def test_basis_gates_multiple_gates(self):
        """Test that basis_gates with multiple gates is accepted."""
        options = {"basis_gates": ["u1", "u2", "u3", "cx"]}
        model = SimulatorOptionsModel.model_validate(options)
        assert model.basis_gates == ["u1", "u2", "u3", "cx"]

    def test_extra_fields_forbidden(self):
        """Test that extra fields are forbidden."""
        options = {"extra_field": "not allowed"}
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            SimulatorOptionsModel.model_validate(options)

    def test_all_options_together(self):
        """Test that all options can be set together."""
        options = {
            "noise_model": {
                "__type__": "NoiseModel",
                "__value__": {"errors": []},
            },
            "seed_simulator": 999,
            "coupling_map": [[0, 1], [1, 2], [2, 0]],
            "basis_gates": ["cx", "id", "rz", "sx", "x"],
        }
        model = SimulatorOptionsModel.model_validate(options)
        assert model.noise_model is not None
        assert model.seed_simulator == 999
        assert model.coupling_map == [[0, 1], [1, 2], [2, 0]]
        assert model.basis_gates == ["cx", "id", "rz", "sx", "x"]


# Made with Bob