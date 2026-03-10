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

"""Validation tests for primitive_result_model.py classes."""

import pytest
from pydantic import ValidationError

from ibm_quantum_schemas.models.estimator.version_0_1_dev.data_bin_model import (
    DataBinModel,
    DataBinObjectModel,
    DataBinWrapperModel,
)
from ibm_quantum_schemas.models.estimator.version_0_1_dev.dynamical_decoupling_metadata_model import (  # noqa: E501
    DynamicalDecouplingMetadataModel,
)
from ibm_quantum_schemas.models.estimator.version_0_1_dev.primitive_result_model import (
    PrimitiveResultMetadataModel,
    PrimitiveResultModel,
    PrimitiveResultWrapperModel,
)
from ibm_quantum_schemas.models.estimator.version_0_1_dev.primitive_result_resilience_metadata_model import (  # noqa: E501
    PrimitiveResultResilienceMetadataModel,
)
from ibm_quantum_schemas.models.estimator.version_0_1_dev.pub_result_model import (
    PubResultMetadataModel,
    PubResultModel,
    PubResultWrapperModel,
)
from ibm_quantum_schemas.models.estimator.version_0_1_dev.twirling_metadata_model import (
    TwirlingMetadataModel,
)


class TestPrimitiveResultMetadataModelValidation:
    """Test PrimitiveResultMetadataModel validation."""

    def test_valid_metadata_with_defaults(self):
        """Test that metadata with default values is accepted."""
        model = PrimitiveResultMetadataModel.model_validate({})
        assert model.dynamical_decoupling is None
        assert model.twirling is None
        assert model.resilience is None
        assert model.version == 2

    def test_valid_with_dynamical_decoupling(self):
        """Test that metadata with dynamical_decoupling is valid."""
        dd_data = DynamicalDecouplingMetadataModel.model_validate({"enable": True})
        data = {"dynamical_decoupling": dd_data}
        model = PrimitiveResultMetadataModel.model_validate(data)
        assert model.dynamical_decoupling == dd_data
        assert model.dynamical_decoupling.enable is True

    def test_dynamical_decoupling_none(self):
        """Test that dynamical_decoupling can be None."""
        data = {"dynamical_decoupling": None}
        model = PrimitiveResultMetadataModel.model_validate(data)
        assert model.dynamical_decoupling is None

    def test_valid_with_twirling(self):
        """Test that metadata with twirling is valid."""
        twirling_data = TwirlingMetadataModel.model_validate({"enable_gates": True})
        data = {"twirling": twirling_data}
        model = PrimitiveResultMetadataModel.model_validate(data)
        assert model.twirling == twirling_data
        assert model.twirling.enable_gates is True

    def test_twirling_none(self):
        """Test that twirling can be None."""
        data = {"twirling": None}
        model = PrimitiveResultMetadataModel.model_validate(data)
        assert model.twirling is None

    def test_valid_with_resilience(self):
        """Test that metadata with resilience is valid."""
        resilience_data = PrimitiveResultResilienceMetadataModel.model_validate(
            {"measure_mitigation": True}
        )
        data = {"resilience": resilience_data}
        model = PrimitiveResultMetadataModel.model_validate(data)
        assert model.resilience == resilience_data
        assert model.resilience.measure_mitigation is True

    def test_resilience_none(self):
        """Test that resilience can be None."""
        data = {"resilience": None}
        model = PrimitiveResultMetadataModel.model_validate(data)
        assert model.resilience is None

    def test_version_default(self):
        """Test that version defaults to 2."""
        model = PrimitiveResultMetadataModel.model_validate({})
        assert model.version == 2

    def test_version_explicit(self):
        """Test that version can be explicitly set to 2."""
        data = {"version": 2}
        model = PrimitiveResultMetadataModel.model_validate(data)
        assert model.version == 2

    def test_invalid_version(self):
        """Test that invalid version is rejected."""
        data = {"version": 1}
        with pytest.raises(ValidationError, match="Input should be 2"):
            PrimitiveResultMetadataModel.model_validate(data)

    def test_all_fields_together(self):
        """Test that all fields can be set together."""
        dd_data = DynamicalDecouplingMetadataModel.model_validate(
            {"enable": True, "sequence_type": "XY4"}
        )
        twirling_data = TwirlingMetadataModel.model_validate(
            {"enable_gates": True, "num_randomizations": 100}
        )
        resilience_data = PrimitiveResultResilienceMetadataModel.model_validate(
            {"measure_mitigation": True, "zne_mitigation": False}
        )
        data = {
            "dynamical_decoupling": dd_data,
            "twirling": twirling_data,
            "resilience": resilience_data,
            "version": 2,
        }
        model = PrimitiveResultMetadataModel.model_validate(data)
        assert model.dynamical_decoupling == dd_data
        assert model.twirling == twirling_data
        assert model.resilience == resilience_data
        assert model.version == 2


class TestPrimitiveResultModelValidation:
    """Test PrimitiveResultModel validation."""

    def test_valid_primitive_result(self, valid_ndarray_wrapper):
        """Test that a valid primitive result is accepted."""
        # Create a pub result
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
        pub_metadata = PubResultMetadataModel.model_validate({})
        pub_result = PubResultModel.model_validate(
            {
                "data": data_bin_wrapper,
                "metadata": pub_metadata,
            }
        )
        pub_result_wrapper = PubResultWrapperModel.model_validate({"__value__": pub_result})

        # Create primitive result
        metadata = PrimitiveResultMetadataModel.model_validate({})
        data = {
            "pub_results": [pub_result_wrapper],
            "metadata": metadata,
        }
        model = PrimitiveResultModel.model_validate(data)
        assert len(model.pub_results) == 1
        assert model.pub_results[0] == pub_result_wrapper
        assert model.metadata == metadata

    def test_valid_with_multiple_pub_results(self, valid_ndarray_wrapper):
        """Test primitive result with multiple pub results."""
        # Create pub results
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
        pub_metadata = PubResultMetadataModel.model_validate({})
        pub_result = PubResultModel.model_validate(
            {
                "data": data_bin_wrapper,
                "metadata": pub_metadata,
            }
        )
        pub_result_wrapper = PubResultWrapperModel.model_validate({"__value__": pub_result})

        # Create primitive result with multiple pubs
        metadata = PrimitiveResultMetadataModel.model_validate({})
        data = {
            "pub_results": [pub_result_wrapper, pub_result_wrapper, pub_result_wrapper],
            "metadata": metadata,
        }
        model = PrimitiveResultModel.model_validate(data)
        assert len(model.pub_results) == 3

    def test_valid_with_empty_pub_results(self):
        """Test primitive result with empty pub_results list."""
        metadata = PrimitiveResultMetadataModel.model_validate({})
        data = {
            "pub_results": [],
            "metadata": metadata,
        }
        model = PrimitiveResultModel.model_validate(data)
        assert len(model.pub_results) == 0

    def test_valid_with_full_metadata(self, valid_ndarray_wrapper):
        """Test primitive result with full metadata."""
        # Create a pub result
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
        pub_metadata = PubResultMetadataModel.model_validate({})
        pub_result = PubResultModel.model_validate(
            {
                "data": data_bin_wrapper,
                "metadata": pub_metadata,
            }
        )
        pub_result_wrapper = PubResultWrapperModel.model_validate({"__value__": pub_result})

        # Create full metadata
        dd_data = DynamicalDecouplingMetadataModel.model_validate({"enable": True})
        twirling_data = TwirlingMetadataModel.model_validate({"enable_gates": True})
        resilience_data = PrimitiveResultResilienceMetadataModel.model_validate(
            {"measure_mitigation": True}
        )
        metadata = PrimitiveResultMetadataModel.model_validate(
            {
                "dynamical_decoupling": dd_data,
                "twirling": twirling_data,
                "resilience": resilience_data,
            }
        )

        data = {
            "pub_results": [pub_result_wrapper],
            "metadata": metadata,
        }
        model = PrimitiveResultModel.model_validate(data)
        assert model.metadata.dynamical_decoupling == dd_data
        assert model.metadata.twirling == twirling_data
        assert model.metadata.resilience == resilience_data

    def test_missing_required_pub_results(self):
        """Test that missing pub_results is rejected."""
        metadata = PrimitiveResultMetadataModel.model_validate({})
        data = {"metadata": metadata}
        with pytest.raises(ValidationError, match="Field required"):
            PrimitiveResultModel.model_validate(data)

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
        pub_metadata = PubResultMetadataModel.model_validate({})
        pub_result = PubResultModel.model_validate(
            {
                "data": data_bin_wrapper,
                "metadata": pub_metadata,
            }
        )
        pub_result_wrapper = PubResultWrapperModel.model_validate({"__value__": pub_result})

        data = {"pub_results": [pub_result_wrapper]}
        with pytest.raises(ValidationError, match="Field required"):
            PrimitiveResultModel.model_validate(data)


class TestPrimitiveResultWrapperModelValidation:
    """Test PrimitiveResultWrapperModel validation."""

    def test_valid_wrapper_with_defaults(self, valid_ndarray_wrapper):
        """Test that a valid wrapper with default type is accepted."""
        # Create a pub result
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
        pub_metadata = PubResultMetadataModel.model_validate({})
        pub_result = PubResultModel.model_validate(
            {
                "data": data_bin_wrapper,
                "metadata": pub_metadata,
            }
        )
        pub_result_wrapper = PubResultWrapperModel.model_validate({"__value__": pub_result})

        # Create primitive result
        metadata = PrimitiveResultMetadataModel.model_validate({})
        value = PrimitiveResultModel.model_validate(
            {
                "pub_results": [pub_result_wrapper],
                "metadata": metadata,
            }
        )
        data = {"__value__": value}
        model = PrimitiveResultWrapperModel.model_validate(data)
        assert model.type_ == "PrimitiveResult"
        assert len(model.value_.pub_results) == 1

    def test_valid_wrapper_with_explicit_type(self, valid_ndarray_wrapper):
        """Test that a valid wrapper with explicit type is accepted."""
        # Create a pub result
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
        pub_metadata = PubResultMetadataModel.model_validate({})
        pub_result = PubResultModel.model_validate(
            {
                "data": data_bin_wrapper,
                "metadata": pub_metadata,
            }
        )
        pub_result_wrapper = PubResultWrapperModel.model_validate({"__value__": pub_result})

        # Create primitive result
        metadata = PrimitiveResultMetadataModel.model_validate({})
        value = PrimitiveResultModel.model_validate(
            {
                "pub_results": [pub_result_wrapper],
                "metadata": metadata,
            }
        )
        data = {
            "__type__": "PrimitiveResult",
            "__value__": value,
        }
        model = PrimitiveResultWrapperModel.model_validate(data)
        assert model.type_ == "PrimitiveResult"

    def test_invalid_type(self, valid_ndarray_wrapper):
        """Test that invalid type is rejected."""
        # Create a pub result
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
        pub_metadata = PubResultMetadataModel.model_validate({})
        pub_result = PubResultModel.model_validate(
            {
                "data": data_bin_wrapper,
                "metadata": pub_metadata,
            }
        )
        pub_result_wrapper = PubResultWrapperModel.model_validate({"__value__": pub_result})

        # Create primitive result
        metadata = PrimitiveResultMetadataModel.model_validate({})
        value = PrimitiveResultModel.model_validate(
            {
                "pub_results": [pub_result_wrapper],
                "metadata": metadata,
            }
        )
        data = {
            "__type__": "InvalidType",
            "__value__": value,
        }
        with pytest.raises(ValidationError, match="Input should be 'PrimitiveResult'"):
            PrimitiveResultWrapperModel.model_validate(data)

    def test_missing_required_value(self):
        """Test that missing value is rejected."""
        data = {"__type__": "PrimitiveResult"}
        with pytest.raises(ValidationError, match="Field required"):
            PrimitiveResultWrapperModel.model_validate(data)

    def test_serialization_uses_aliases(self, valid_ndarray_wrapper):
        """Test that serialization uses aliases."""
        # Create a pub result
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
        pub_metadata = PubResultMetadataModel.model_validate({})
        pub_result = PubResultModel.model_validate(
            {
                "data": data_bin_wrapper,
                "metadata": pub_metadata,
            }
        )
        pub_result_wrapper = PubResultWrapperModel.model_validate({"__value__": pub_result})

        # Create primitive result
        metadata = PrimitiveResultMetadataModel.model_validate({})
        value = PrimitiveResultModel.model_validate(
            {
                "pub_results": [pub_result_wrapper],
                "metadata": metadata,
            }
        )
        model = PrimitiveResultWrapperModel.model_validate({"__value__": value})
        serialized = model.model_dump(mode="json")
        assert "__type__" in serialized
        assert "__value__" in serialized
        assert "type_" not in serialized
        assert "value_" not in serialized
