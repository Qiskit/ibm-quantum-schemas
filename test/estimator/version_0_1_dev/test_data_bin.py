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

"""Validation tests for data_bin_model.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.common.ndarray_wrapper import NdarrayWrapperModel
from ibm_quantum_schemas.estimator.version_0_1_dev.data_bin import (
    DataBinModel,
    DataBinObjectModel,
    DataBinWrapperModel,
)


class TestDataBinObjectModelValidation:
    """Test DataBinObjectModel validation."""

    def test_valid_empty_object(self):
        """Test that an empty data bin object is valid."""
        model = DataBinObjectModel.model_validate({})
        assert model.evs is None
        assert model.stds is None
        assert model.evs_noise_factors is None
        assert model.stds_noise_factors is None
        assert model.ensemble_stds_noise_factors is None
        assert model.evs_extrapolated is None
        assert model.stds_extrapolated is None
        assert model.ensemble_standard_error is None

    def test_valid_with_evs(self, valid_ndarray_wrapper):
        """Test that data bin object with evs is valid."""
        data = {"evs": valid_ndarray_wrapper}
        model = DataBinObjectModel.model_validate(data)
        expected_evs = NdarrayWrapperModel.model_validate(valid_ndarray_wrapper)
        assert model.evs == expected_evs
        assert model.stds is None

    def test_valid_with_all_fields(self, valid_ndarray_wrapper):
        """Test that data bin object with all fields is valid."""
        data = {
            "evs": valid_ndarray_wrapper,
            "stds": valid_ndarray_wrapper,
            "evs_noise_factors": valid_ndarray_wrapper,
            "stds_noise_factors": valid_ndarray_wrapper,
            "ensemble_stds_noise_factors": valid_ndarray_wrapper,
            "evs_extrapolated": valid_ndarray_wrapper,
            "stds_extrapolated": valid_ndarray_wrapper,
            "ensemble_standard_error": valid_ndarray_wrapper,
        }
        model = DataBinObjectModel.model_validate(data)
        expected = NdarrayWrapperModel.model_validate(valid_ndarray_wrapper)
        assert model.evs == expected
        assert model.stds == expected
        assert model.evs_noise_factors == expected
        assert model.stds_noise_factors == expected
        assert model.ensemble_stds_noise_factors == expected
        assert model.evs_extrapolated == expected
        assert model.stds_extrapolated == expected
        assert model.ensemble_standard_error == expected


class TestDataBinModelValidation:
    """Test DataBinModel validation."""

    def test_valid_data_bin(self, valid_ndarray_wrapper):
        """Test that a valid data bin is accepted."""
        fields = DataBinObjectModel.model_validate({"evs": valid_ndarray_wrapper})
        data = {
            "field_names": ["evs"],
            "field_types": ["ndarray"],
            "shape": (10,),
            "fields": fields,
        }
        model = DataBinModel.model_validate(data)
        assert model.field_names == ["evs"]
        assert model.field_types == ["ndarray"]
        assert model.shape == (10,)
        expected_evs = NdarrayWrapperModel.model_validate(valid_ndarray_wrapper)
        assert model.fields.evs == expected_evs

    def test_valid_with_multiple_fields(self, valid_ndarray_wrapper):
        """Test data bin with multiple fields."""
        fields = DataBinObjectModel.model_validate(
            {
                "evs": valid_ndarray_wrapper,
                "stds": valid_ndarray_wrapper,
            }
        )
        data = {
            "field_names": ["evs", "stds"],
            "field_types": ["ndarray", "ndarray"],
            "shape": (5, 3),
            "fields": fields,
        }
        model = DataBinModel.model_validate(data)
        assert len(model.field_names) == 2
        assert len(model.field_types) == 2
        assert model.shape == (5, 3)

    def test_missing_required_field_names(self):
        """Test that missing field_names is rejected."""
        fields = DataBinObjectModel.model_validate({})
        data = {
            "field_types": ["ndarray"],
            "shape": (10,),
            "fields": fields,
        }
        with pytest.raises(ValidationError, match="Field required"):
            DataBinModel.model_validate(data)

    def test_missing_required_field_types(self):
        """Test that missing field_types is rejected."""
        fields = DataBinObjectModel.model_validate({})
        data = {
            "field_names": ["evs"],
            "shape": (10,),
            "fields": fields,
        }
        with pytest.raises(ValidationError, match="Field required"):
            DataBinModel.model_validate(data)

    def test_missing_required_shape(self):
        """Test that missing shape is rejected."""
        fields = DataBinObjectModel.model_validate({})
        data = {
            "field_names": ["evs"],
            "field_types": ["ndarray"],
            "fields": fields,
        }
        with pytest.raises(ValidationError, match="Field required"):
            DataBinModel.model_validate(data)

    def test_missing_required_fields(self):
        """Test that missing fields is rejected."""
        data = {
            "field_names": ["evs"],
            "field_types": ["ndarray"],
            "shape": (10,),
        }
        with pytest.raises(ValidationError, match="Field required"):
            DataBinModel.model_validate(data)


class TestDataBinWrapperModelValidation:
    """Test DataBinWrapperModel validation."""

    def test_valid_wrapper_with_defaults(self, valid_ndarray_wrapper):
        """Test that a valid wrapper with default type is accepted."""
        fields = DataBinObjectModel.model_validate({"evs": valid_ndarray_wrapper})
        value = DataBinModel.model_validate(
            {
                "field_names": ["evs"],
                "field_types": ["ndarray"],
                "shape": (10,),
                "fields": fields,
            }
        )
        data = {"__value__": value}
        model = DataBinWrapperModel.model_validate(data)
        assert model.type_ == "DataBin"
        assert model.value_.field_names == ["evs"]

    def test_valid_wrapper_with_explicit_type(self, valid_ndarray_wrapper):
        """Test that a valid wrapper with explicit type is accepted."""
        fields = DataBinObjectModel.model_validate({"evs": valid_ndarray_wrapper})
        value = DataBinModel.model_validate(
            {
                "field_names": ["evs"],
                "field_types": ["ndarray"],
                "shape": (10,),
                "fields": fields,
            }
        )
        data = {
            "__type__": "DataBin",
            "__value__": value,
        }
        model = DataBinWrapperModel.model_validate(data)
        assert model.type_ == "DataBin"

    def test_invalid_type(self):
        """Test that invalid type is rejected."""
        fields = DataBinObjectModel.model_validate({})
        value = DataBinModel.model_validate(
            {
                "field_names": [],
                "field_types": [],
                "shape": (),
                "fields": fields,
            }
        )
        data = {
            "__type__": "InvalidType",
            "__value__": value,
        }
        with pytest.raises(ValidationError, match="Input should be 'DataBin'"):
            DataBinWrapperModel.model_validate(data)

    def test_missing_required_value(self):
        """Test that missing value is rejected."""
        data = {"__type__": "DataBin"}
        with pytest.raises(ValidationError, match="Field required"):
            DataBinWrapperModel.model_validate(data)

    def test_serialization_uses_aliases(self, valid_ndarray_wrapper):
        """Test that serialization uses aliases."""
        fields = DataBinObjectModel.model_validate({"evs": valid_ndarray_wrapper})
        value = DataBinModel.model_validate(
            {
                "field_names": ["evs"],
                "field_types": ["ndarray"],
                "shape": (10,),
                "fields": fields,
            }
        )
        model = DataBinWrapperModel.model_validate({"__value__": value})
        serialized = model.model_dump(mode="json")
        assert "__type__" in serialized
        assert "__value__" in serialized
        assert "type_" not in serialized
        assert "value_" not in serialized
