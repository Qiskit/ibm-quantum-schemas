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

"""Validation tests for pub_result_model.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.models.estimator.version_0_1_dev.output.data_bin_model import (
    DataBinModel,
    DataBinObjectModel,
    DataBinWrapperModel,
)
from ibm_quantum_schemas.models.estimator.version_0_1_dev.output.pub_result_model import (
    PubResultMetadataModel,
    PubResultModel,
    PubResultWrapperModel,
)
from ibm_quantum_schemas.models.estimator.version_0_1_dev.output.pub_result_resilience_metadata_model import (
    PubResultResilienceMetadataModel,
)


class TestPubResultMetadataModelValidation:
    """Test PubResultMetadataModel validation."""

    def test_valid_empty_metadata(self):
        """Test that empty metadata is valid."""
        model = PubResultMetadataModel.model_validate({})
        assert model.circuit_metadata is None
        assert model.target_precision is None
        assert model.shots is None
        assert model.num_randomizations is None
        assert model.resilience is None
        assert model.experimental is None

    def test_valid_with_circuit_metadata(self):
        """Test that metadata with circuit_metadata is valid."""
        data = {"circuit_metadata": {"key": "value"}}
        model = PubResultMetadataModel.model_validate(data)
        assert model.circuit_metadata == {"key": "value"}

    def test_circuit_metadata_empty_dict(self):
        """Test that circuit_metadata accepts empty dict."""
        data = {"circuit_metadata": {}}
        model = PubResultMetadataModel.model_validate(data)
        assert model.circuit_metadata == {}

    def test_circuit_metadata_none(self):
        """Test that circuit_metadata can be None."""
        data = {"circuit_metadata": None}
        model = PubResultMetadataModel.model_validate(data)
        assert model.circuit_metadata is None

    def test_valid_with_target_precision(self):
        """Test that metadata with target_precision is valid."""
        data = {"target_precision": 0.01}
        model = PubResultMetadataModel.model_validate(data)
        assert model.target_precision == 0.01

    def test_target_precision_zero(self):
        """Test that target_precision can be zero."""
        data = {"target_precision": 0.0}
        model = PubResultMetadataModel.model_validate(data)
        assert model.target_precision == 0.0

    def test_target_precision_none(self):
        """Test that target_precision can be None."""
        data = {"target_precision": None}
        model = PubResultMetadataModel.model_validate(data)
        assert model.target_precision is None

    def test_valid_with_shots(self):
        """Test that metadata with shots is valid."""
        data = {"shots": 1024}
        model = PubResultMetadataModel.model_validate(data)
        assert model.shots == 1024

    def test_shots_none(self):
        """Test that shots can be None."""
        data = {"shots": None}
        model = PubResultMetadataModel.model_validate(data)
        assert model.shots is None

    def test_valid_with_num_randomizations(self):
        """Test that metadata with num_randomizations is valid."""
        data = {"num_randomizations": 100}
        model = PubResultMetadataModel.model_validate(data)
        assert model.num_randomizations == 100

    def test_num_randomizations_none(self):
        """Test that num_randomizations can be None."""
        data = {"num_randomizations": None}
        model = PubResultMetadataModel.model_validate(data)
        assert model.num_randomizations is None

    def test_valid_with_resilience(self):
        """Test that metadata with resilience is valid."""
        resilience_data = PubResultResilienceMetadataModel.model_validate({})
        data = {"resilience": resilience_data}
        model = PubResultMetadataModel.model_validate(data)
        assert model.resilience == resilience_data

    def test_resilience_none(self):
        """Test that resilience can be None."""
        data = {"resilience": None}
        model = PubResultMetadataModel.model_validate(data)
        assert model.resilience is None

    def test_valid_with_experimental(self):
        """Test that metadata with experimental is valid."""
        data = {"experimental": {"feature": "test"}}
        model = PubResultMetadataModel.model_validate(data)
        assert model.experimental == {"feature": "test"}

    def test_experimental_empty_dict(self):
        """Test that experimental accepts empty dict."""
        data = {"experimental": {}}
        model = PubResultMetadataModel.model_validate(data)
        assert model.experimental == {}

    def test_experimental_none(self):
        """Test that experimental can be None."""
        data = {"experimental": None}
        model = PubResultMetadataModel.model_validate(data)
        assert model.experimental is None

    def test_all_fields_together(self):
        """Test that all fields can be set together."""
        resilience_data = PubResultResilienceMetadataModel.model_validate({})
        data = {
            "circuit_metadata": {"name": "test_circuit"},
            "target_precision": 0.05,
            "shots": 2048,
            "num_randomizations": 50,
            "resilience": resilience_data,
            "experimental": {"debug": True},
        }
        model = PubResultMetadataModel.model_validate(data)
        assert model.circuit_metadata == {"name": "test_circuit"}
        assert model.target_precision == 0.05
        assert model.shots == 2048
        assert model.num_randomizations == 50
        assert model.resilience == resilience_data
        assert model.experimental == {"debug": True}

    def test_extra_fields_forbidden(self):
        """Test that extra fields are forbidden."""
        data = {"extra_field": "not allowed"}
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            PubResultMetadataModel.model_validate(data)


class TestPubResultModelValidation:
    """Test PubResultModel validation."""

    def test_valid_pub_result(self, valid_ndarray_wrapper):
        """Test that a valid pub result is accepted."""
        fields = DataBinObjectModel.model_validate({"evs": valid_ndarray_wrapper})
        data_bin = DataBinModel.model_validate(
            {
                "field_names": ["evs"],
                "field_types": ["ndarray"],
                "shape": (10,),
                "fields": fields,
            }
        )
        data_bin_wrapper = DataBinWrapperModel.model_validate({"__value__": data_bin})
        metadata = PubResultMetadataModel.model_validate({})

        data = {
            "data": data_bin_wrapper,
            "metadata": metadata,
        }
        model = PubResultModel.model_validate(data)
        assert model.data == data_bin_wrapper
        assert model.metadata == metadata

    def test_valid_with_full_metadata(self, valid_ndarray_wrapper):
        """Test pub result with full metadata."""
        fields = DataBinObjectModel.model_validate({"evs": valid_ndarray_wrapper})
        data_bin = DataBinModel.model_validate(
            {
                "field_names": ["evs"],
                "field_types": ["ndarray"],
                "shape": (5,),
                "fields": fields,
            }
        )
        data_bin_wrapper = DataBinWrapperModel.model_validate({"__value__": data_bin})

        resilience_data = PubResultResilienceMetadataModel.model_validate({})
        metadata = PubResultMetadataModel.model_validate(
            {
                "circuit_metadata": {"id": "circuit_1"},
                "target_precision": 0.01,
                "shots": 1024,
                "num_randomizations": 100,
                "resilience": resilience_data,
                "experimental": {"test": True},
            }
        )

        data = {
            "data": data_bin_wrapper,
            "metadata": metadata,
        }
        model = PubResultModel.model_validate(data)
        assert model.metadata.shots == 1024
        assert model.metadata.target_precision == 0.01

    def test_missing_required_data(self):
        """Test that missing data is rejected."""
        metadata = PubResultMetadataModel.model_validate({})
        data = {"metadata": metadata}
        with pytest.raises(ValidationError, match="Field required"):
            PubResultModel.model_validate(data)

    def test_missing_required_metadata(self, valid_ndarray_wrapper):
        """Test that missing metadata is rejected."""
        fields = DataBinObjectModel.model_validate({"evs": valid_ndarray_wrapper})
        data_bin = DataBinModel.model_validate(
            {
                "field_names": ["evs"],
                "field_types": ["ndarray"],
                "shape": (10,),
                "fields": fields,
            }
        )
        data_bin_wrapper = DataBinWrapperModel.model_validate({"__value__": data_bin})

        data = {"data": data_bin_wrapper}
        with pytest.raises(ValidationError, match="Field required"):
            PubResultModel.model_validate(data)

    def test_extra_fields_forbidden(self, valid_ndarray_wrapper):
        """Test that extra fields are forbidden."""
        fields = DataBinObjectModel.model_validate({"evs": valid_ndarray_wrapper})
        data_bin = DataBinModel.model_validate(
            {
                "field_names": ["evs"],
                "field_types": ["ndarray"],
                "shape": (10,),
                "fields": fields,
            }
        )
        data_bin_wrapper = DataBinWrapperModel.model_validate({"__value__": data_bin})
        metadata = PubResultMetadataModel.model_validate({})

        data = {
            "data": data_bin_wrapper,
            "metadata": metadata,
            "extra_field": "not allowed",
        }
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            PubResultModel.model_validate(data)


class TestPubResultWrapperModelValidation:
    """Test PubResultWrapperModel validation."""

    def test_valid_wrapper_with_defaults(self, valid_ndarray_wrapper):
        """Test that a valid wrapper with default type is accepted."""
        fields = DataBinObjectModel.model_validate({"evs": valid_ndarray_wrapper})
        data_bin = DataBinModel.model_validate(
            {
                "field_names": ["evs"],
                "field_types": ["ndarray"],
                "shape": (10,),
                "fields": fields,
            }
        )
        data_bin_wrapper = DataBinWrapperModel.model_validate({"__value__": data_bin})
        metadata = PubResultMetadataModel.model_validate({})

        value = PubResultModel.model_validate(
            {
                "data": data_bin_wrapper,
                "metadata": metadata,
            }
        )
        data = {"__value__": value}
        model = PubResultWrapperModel.model_validate(data)
        assert model.type_ == "PubResult"
        assert model.value_ == value
        assert model.value_.data == data_bin_wrapper

    def test_valid_wrapper_with_explicit_type(self, valid_ndarray_wrapper):
        """Test that a valid wrapper with explicit type is accepted."""
        fields = DataBinObjectModel.model_validate({"evs": valid_ndarray_wrapper})
        data_bin = DataBinModel.model_validate(
            {
                "field_names": ["evs"],
                "field_types": ["ndarray"],
                "shape": (10,),
                "fields": fields,
            }
        )
        data_bin_wrapper = DataBinWrapperModel.model_validate({"__value__": data_bin})
        metadata = PubResultMetadataModel.model_validate({})

        value = PubResultModel.model_validate(
            {
                "data": data_bin_wrapper,
                "metadata": metadata,
            }
        )
        data = {
            "__type__": "PubResult",
            "__value__": value,
        }
        model = PubResultWrapperModel.model_validate(data)
        assert model.type_ == "PubResult"

    def test_invalid_type(self, valid_ndarray_wrapper):
        """Test that invalid type is rejected."""
        fields = DataBinObjectModel.model_validate({"evs": valid_ndarray_wrapper})
        data_bin = DataBinModel.model_validate(
            {
                "field_names": ["evs"],
                "field_types": ["ndarray"],
                "shape": (10,),
                "fields": fields,
            }
        )
        data_bin_wrapper = DataBinWrapperModel.model_validate({"__value__": data_bin})
        metadata = PubResultMetadataModel.model_validate({})

        value = PubResultModel.model_validate(
            {
                "data": data_bin_wrapper,
                "metadata": metadata,
            }
        )
        data = {
            "__type__": "InvalidType",
            "__value__": value,
        }
        with pytest.raises(ValidationError, match="Input should be 'PubResult'"):
            PubResultWrapperModel.model_validate(data)

    def test_missing_required_value(self):
        """Test that missing value is rejected."""
        data = {"__type__": "PubResult"}
        with pytest.raises(ValidationError, match="Field required"):
            PubResultWrapperModel.model_validate(data)

    def test_serialization_uses_aliases(self, valid_ndarray_wrapper):
        """Test that serialization uses aliases."""
        fields = DataBinObjectModel.model_validate({"evs": valid_ndarray_wrapper})
        data_bin = DataBinModel.model_validate(
            {
                "field_names": ["evs"],
                "field_types": ["ndarray"],
                "shape": (10,),
                "fields": fields,
            }
        )
        data_bin_wrapper = DataBinWrapperModel.model_validate({"__value__": data_bin})
        metadata = PubResultMetadataModel.model_validate({})

        value = PubResultModel.model_validate(
            {
                "data": data_bin_wrapper,
                "metadata": metadata,
            }
        )
        model = PubResultWrapperModel.model_validate({"__value__": value})
        serialized = model.model_dump(mode="json")
        assert "__type__" in serialized
        assert "__value__" in serialized
        assert "type_" not in serialized
        assert "value_" not in serialized

    def test_extra_fields_forbidden(self, valid_ndarray_wrapper):
        """Test that extra fields are forbidden."""
        fields = DataBinObjectModel.model_validate({"evs": valid_ndarray_wrapper})
        data_bin = DataBinModel.model_validate(
            {
                "field_names": ["evs"],
                "field_types": ["ndarray"],
                "shape": (10,),
                "fields": fields,
            }
        )
        data_bin_wrapper = DataBinWrapperModel.model_validate({"__value__": data_bin})
        metadata = PubResultMetadataModel.model_validate({})

        value = PubResultModel.model_validate(
            {
                "data": data_bin_wrapper,
                "metadata": metadata,
            }
        )
        data = {
            "__value__": value,
            "extra_field": "not allowed",
        }
        with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
            PubResultWrapperModel.model_validate(data)
