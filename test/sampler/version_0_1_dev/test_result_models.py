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

"""Tests for Sampler V2 result models."""

import base64
import io
import zlib
from datetime import datetime

import numpy as np

from ibm_quantum_schemas.common.datetime_wrapper import DatetimeWrapperModel
from ibm_quantum_schemas.common.ndarray_wrapper import NdarrayWrapperModel
from ibm_quantum_schemas.sampler.version_0_1_dev.bit_array import (
    BitArrayModel,
    BitArrayWrapperModel,
)
from ibm_quantum_schemas.sampler.version_0_1_dev.data_bin import (
    DataBinModel,
    DataBinWrapperModel,
)
from ibm_quantum_schemas.sampler.version_0_1_dev.execution_span import (
    DoubleSliceSpanModel,
    DoubleSliceSpanWrapperModel,
    ExecutionSpansModel,
    ExecutionSpansWrapperModel,
    TwirledSliceSpanV2Model,
    TwirledSliceSpanV2WrapperModel,
)
from ibm_quantum_schemas.sampler.version_0_1_dev.primitive_result import (
    ExecutionMetadataModel,
    PrimitiveResultMetadataModel,
    PrimitiveResultModel,
    PrimitiveResultWrapperModel,
)
from ibm_quantum_schemas.sampler.version_0_1_dev.pub_result import (
    PubResultMetadataModel,
    PubResultModel,
    PubResultWrapperModel,
)


def encode_ndarray(arr: np.ndarray) -> str:
    """Encode a numpy array to base64 string (mimics wire format)."""
    buffer = io.BytesIO()
    np.save(buffer, arr, allow_pickle=False)
    compressed = zlib.compress(buffer.getvalue())
    return base64.b64encode(compressed).decode("utf-8")


def wrap_datetime(dt: datetime) -> DatetimeWrapperModel:
    """Wrap a datetime object in DatetimeWrapperModel format."""
    return DatetimeWrapperModel(type_="datetime", value_=dt.isoformat())


class TestBitArrayModel:
    """Test BitArray models."""

    def test_bit_array_model_creation(self):
        """Test creating a BitArrayModel."""
        # Create a simple bit array (2 shots, 3 bits)
        arr = np.array([[0b101], [0b011]], dtype=np.uint8)
        encoded = encode_ndarray(arr)

        ndarray_wrapper = NdarrayWrapperModel.model_validate(
            {"__type__": "ndarray", "__value__": encoded}
        )
        bit_array = BitArrayModel(num_bits=3, array=ndarray_wrapper)

        assert bit_array.num_bits == 3
        assert bit_array.array.type_ == "ndarray"

    def test_bit_array_wrapper_model_with_defaults(self):
        """Test BitArrayWrapperModel with default type."""
        arr = np.array([[0b101]], dtype=np.uint8)
        encoded = encode_ndarray(arr)

        ndarray_wrapper = NdarrayWrapperModel.model_validate({"__value__": encoded})
        bit_array = BitArrayModel(num_bits=3, array=ndarray_wrapper)
        data = {"__value__": bit_array}
        wrapper = BitArrayWrapperModel.model_validate(data)

        assert wrapper.type_ == "BitArray"
        assert wrapper.value_.num_bits == 3

    def test_bit_array_wrapper_serialization_uses_aliases(self):
        """Test that serialization uses aliases."""
        arr = np.array([[0b101]], dtype=np.uint8)
        encoded = encode_ndarray(arr)

        ndarray_wrapper = NdarrayWrapperModel.model_validate({"__value__": encoded})
        bit_array = BitArrayModel(num_bits=3, array=ndarray_wrapper)
        wrapper = BitArrayWrapperModel.model_validate({"__value__": bit_array})

        serialized = wrapper.model_dump(mode="json")
        assert "__type__" in serialized
        assert "__value__" in serialized
        assert "type_" not in serialized
        assert "value_" not in serialized
        assert serialized["__type__"] == "BitArray"
        assert serialized["__value__"]["num_bits"] == 3


class TestDataBinModel:
    """Test DataBin models."""

    def test_data_bin_model_creation(self):
        """Test creating a DataBinModel with BitArray fields."""
        arr = np.array([[0b101]], dtype=np.uint8)
        encoded = encode_ndarray(arr)

        ndarray_wrapper = NdarrayWrapperModel.model_validate({"__value__": encoded})
        bit_array = BitArrayModel(num_bits=3, array=ndarray_wrapper)
        bit_array_wrapper = BitArrayWrapperModel.model_validate({"__value__": bit_array})

        data_bin = DataBinModel(
            field_names=["meas"],
            field_types=["<class 'qiskit.primitives.containers.bit_array.BitArray'>"],
            shape=(1,),
            fields={"meas": bit_array_wrapper.model_dump(by_alias=True)},
        )

        assert data_bin.shape == (1,)
        assert "meas" in data_bin.field_names
        assert "meas" in data_bin.fields

    def test_data_bin_wrapper_model_with_defaults(self):
        """Test DataBinWrapperModel with default type."""
        data_bin = DataBinModel(
            field_names=["meas"],
            field_types=["<class 'qiskit.primitives.containers.bit_array.BitArray'>"],
            shape=(2, 3),
            fields={},
        )
        data = {"__value__": data_bin}
        wrapper = DataBinWrapperModel.model_validate(data)

        assert wrapper.type_ == "DataBin"
        assert wrapper.value_.shape == (2, 3)

    def test_data_bin_wrapper_serialization_uses_aliases(self):
        """Test that serialization uses aliases."""
        data_bin = DataBinModel(
            field_names=["meas"],
            field_types=["<class 'qiskit.primitives.containers.bit_array.BitArray'>"],
            shape=(2, 3),
            fields={},
        )
        wrapper = DataBinWrapperModel.model_validate({"__value__": data_bin})

        serialized = wrapper.model_dump(mode="json")
        assert "__type__" in serialized
        assert "__value__" in serialized
        assert "type_" not in serialized
        assert "value_" not in serialized
        assert serialized["__type__"] == "DataBin"
        assert serialized["__value__"]["shape"] == [2, 3]


class TestPubResultModel:
    """Test PubResult models."""

    def test_pub_result_metadata_model(self):
        """Test PubResultMetadataModel."""
        metadata = PubResultMetadataModel(
            circuit_metadata={"test": "value"},
            num_randomizations=32,
        )

        assert metadata.circuit_metadata == {"test": "value"}
        assert metadata.num_randomizations == 32

    def test_pub_result_model_creation(self):
        """Test creating a complete PubResultModel."""
        data_bin = DataBinModel(
            field_names=["meas"],
            field_types=["<class 'qiskit.primitives.containers.bit_array.BitArray'>"],
            shape=(1,),
            fields={},
        )
        data_bin_wrapper = DataBinWrapperModel.model_validate({"__value__": data_bin})

        metadata = PubResultMetadataModel(num_randomizations=32)
        pub_result = PubResultModel(data=data_bin_wrapper, metadata=metadata)

        assert pub_result.metadata.num_randomizations == 32
        assert pub_result.data.type_ == "DataBin"

    def test_pub_result_wrapper_serialization(self):
        """Test PubResultWrapperModel serialization."""
        data_bin = DataBinModel(
            field_names=[],
            field_types=[],
            shape=(),
            fields={},
        )
        data_bin_wrapper = DataBinWrapperModel.model_validate({"__value__": data_bin})
        metadata = PubResultMetadataModel()
        pub_result = PubResultModel(data=data_bin_wrapper, metadata=metadata)
        wrapper = PubResultWrapperModel.model_validate({"__value__": pub_result})

        serialized = wrapper.model_dump(by_alias=True)
        assert serialized["__type__"] == "PubResult"
        assert "__value__" in serialized


class TestPrimitiveResultModel:
    """Test PrimitiveResult models."""

    def test_primitive_result_metadata_model(self):
        """Test PrimitiveResultMetadataModel."""
        # Create empty ExecutionSpans
        spans_model = ExecutionSpansModel(spans=[])
        spans_wrapper = ExecutionSpansWrapperModel.model_validate({"__value__": spans_model})
        execution = ExecutionMetadataModel(execution_spans=spans_wrapper)

        metadata = PrimitiveResultMetadataModel(
            execution=execution,
            version=2,
        )

        assert metadata.version == 2
        assert len(metadata.execution.execution_spans.value_.spans) == 0

    def test_primitive_result_model_creation(self):
        """Test creating a complete PrimitiveResultModel."""
        # Create a simple pub result
        data_bin = DataBinModel(
            field_names=[],
            field_types=[],
            shape=(),
            fields={},
        )
        data_bin_wrapper = DataBinWrapperModel.model_validate({"__value__": data_bin})
        pub_metadata = PubResultMetadataModel()
        pub_result = PubResultModel(data=data_bin_wrapper, metadata=pub_metadata)
        pub_result_wrapper = PubResultWrapperModel.model_validate({"__value__": pub_result})

        # Create primitive result with proper ExecutionSpans
        spans_model = ExecutionSpansModel(spans=[])
        spans_wrapper = ExecutionSpansWrapperModel.model_validate({"__value__": spans_model})
        execution = ExecutionMetadataModel(execution_spans=spans_wrapper)
        metadata = PrimitiveResultMetadataModel(execution=execution, version=2)
        primitive_result = PrimitiveResultModel(
            pub_results=[pub_result_wrapper],
            metadata=metadata,
        )

        assert len(primitive_result.pub_results) == 1
        assert primitive_result.metadata.version == 2

    def test_primitive_result_wrapper_serialization(self):
        """Test complete PrimitiveResultWrapperModel serialization."""
        # Build from bottom up
        data_bin = DataBinModel(
            field_names=["meas"],
            field_types=["<class 'qiskit.primitives.containers.bit_array.BitArray'>"],
            shape=(1,),
            fields={},
        )
        data_bin_wrapper = DataBinWrapperModel.model_validate({"__value__": data_bin})

        pub_metadata = PubResultMetadataModel(num_randomizations=16)
        pub_result = PubResultModel(data=data_bin_wrapper, metadata=pub_metadata)
        pub_result_wrapper = PubResultWrapperModel.model_validate({"__value__": pub_result})

        # Create proper ExecutionSpans
        spans_model = ExecutionSpansModel(spans=[])
        spans_wrapper = ExecutionSpansWrapperModel.model_validate({"__value__": spans_model})
        execution = ExecutionMetadataModel(execution_spans=spans_wrapper)
        prim_metadata = PrimitiveResultMetadataModel(execution=execution, version=2)
        primitive_result = PrimitiveResultModel(
            pub_results=[pub_result_wrapper],
            metadata=prim_metadata,
        )
        wrapper = PrimitiveResultWrapperModel.model_validate({"__value__": primitive_result})

        # Test serialization
        serialized = wrapper.model_dump(by_alias=True)
        assert serialized["__type__"] == "PrimitiveResult"
        assert serialized["__value__"]["metadata"]["version"] == 2
        assert len(serialized["__value__"]["pub_results"]) == 1

        # Verify nested structure
        pub_result_data = serialized["__value__"]["pub_results"][0]
        assert pub_result_data["__type__"] == "PubResult"
        assert pub_result_data["__value__"]["metadata"]["num_randomizations"] == 16


class TestExecutionSpanModels:
    """Test execution span models."""

    def test_double_slice_span_model(self):
        """Test DoubleSliceSpanModel creation."""
        start_dt = wrap_datetime(datetime(2024, 8, 20, 0, 0, 0))
        stop_dt = wrap_datetime(datetime(2024, 8, 21, 0, 0, 0))
        span = DoubleSliceSpanModel(
            start=start_dt,
            stop=stop_dt,
            data_slices={0: [[14], 2, 3, 1, 9]},
        )

        assert span.start.value_ == datetime(2024, 8, 20, 0, 0, 0).isoformat()
        assert span.stop.value_ == datetime(2024, 8, 21, 0, 0, 0).isoformat()
        assert 0 in span.data_slices
        assert span.data_slices[0] == [[14], 2, 3, 1, 9]

    def test_double_slice_span_wrapper_model(self):
        """Test DoubleSliceSpanWrapperModel."""
        span = DoubleSliceSpanModel(
            start=wrap_datetime(datetime(2024, 8, 20)),
            stop=wrap_datetime(datetime(2024, 8, 21)),
            data_slices={0: [[14], 2, 3, 1, 9]},
        )
        wrapper = DoubleSliceSpanWrapperModel.model_validate({"__value__": span})

        assert wrapper.type_ == "DoubleSliceSpan"
        assert wrapper.value_.start.value_ == datetime(2024, 8, 20).isoformat()

    def test_double_slice_span_serialization(self):
        """Test DoubleSliceSpan serialization uses aliases."""
        span = DoubleSliceSpanModel(
            start=wrap_datetime(datetime(2024, 8, 20)),
            stop=wrap_datetime(datetime(2024, 8, 21)),
            data_slices={0: [[14], 2, 3, 1, 9]},
        )
        wrapper = DoubleSliceSpanWrapperModel.model_validate({"__value__": span})

        serialized = wrapper.model_dump(by_alias=True)
        assert "__type__" in serialized
        assert "__value__" in serialized
        assert serialized["__type__"] == "DoubleSliceSpan"
        assert "start" in serialized["__value__"]
        assert "data_slices" in serialized["__value__"]

    def test_twirled_slice_span_v2_model(self):
        """Test TwirledSliceSpanV2Model creation."""
        span = TwirledSliceSpanV2Model(
            start=wrap_datetime(datetime(2024, 9, 20)),
            stop=wrap_datetime(datetime(2024, 9, 21)),
            data_slices={
                0: [[14, 18, 21], True, 2, 3, 1, 9, 200],
                2: [[18, 14, 19], False, 2, 3, 1, 9, 200],
            },
        )

        assert span.start.value_ == datetime(2024, 9, 20).isoformat()
        assert 0 in span.data_slices
        assert 2 in span.data_slices
        assert span.data_slices[0][1] is True  # at_front
        assert span.data_slices[0][6] == 200  # pub_shots
        assert span.data_slices[2][1] is False  # at_front

    def test_twirled_slice_span_v2_wrapper_model(self):
        """Test TwirledSliceSpanV2WrapperModel."""
        span = TwirledSliceSpanV2Model(
            start=wrap_datetime(datetime(2024, 9, 20)),
            stop=wrap_datetime(datetime(2024, 9, 21)),
            data_slices={0: [[14, 18, 21], True, 2, 3, 1, 9, 200]},
        )
        wrapper = TwirledSliceSpanV2WrapperModel.model_validate({"__value__": span})

        assert wrapper.type_ == "TwirledSliceSpanV2"
        assert wrapper.value_.data_slices[0][6] == 200

    def test_execution_spans_model_with_double_slice(self):
        """Test ExecutionSpansModel with DoubleSliceSpan."""
        span = DoubleSliceSpanModel(
            start=wrap_datetime(datetime(2024, 8, 20)),
            stop=wrap_datetime(datetime(2024, 8, 21)),
            data_slices={0: [[14], 2, 3, 1, 9]},
        )
        span_wrapper = DoubleSliceSpanWrapperModel.model_validate({"__value__": span})

        spans_model = ExecutionSpansModel(spans=[span_wrapper])
        assert len(spans_model.spans) == 1
        assert spans_model.spans[0].type_ == "DoubleSliceSpan"

    def test_execution_spans_model_with_twirled_slice(self):
        """Test ExecutionSpansModel with TwirledSliceSpanV2."""
        span = TwirledSliceSpanV2Model(
            start=wrap_datetime(datetime(2024, 9, 20)),
            stop=wrap_datetime(datetime(2024, 9, 21)),
            data_slices={0: [[14, 18, 21], True, 2, 3, 1, 9, 200]},
        )
        span_wrapper = TwirledSliceSpanV2WrapperModel.model_validate({"__value__": span})

        spans_model = ExecutionSpansModel(spans=[span_wrapper])
        assert len(spans_model.spans) == 1
        assert spans_model.spans[0].type_ == "TwirledSliceSpanV2"

    def test_execution_spans_model_with_mixed_spans(self):
        """Test ExecutionSpansModel with both span types."""
        double_span = DoubleSliceSpanModel(
            start=wrap_datetime(datetime(2024, 8, 20)),
            stop=wrap_datetime(datetime(2024, 8, 21)),
            data_slices={0: [[14], 2, 3, 1, 9]},
        )
        double_wrapper = DoubleSliceSpanWrapperModel.model_validate({"__value__": double_span})

        twirled_span = TwirledSliceSpanV2Model(
            start=wrap_datetime(datetime(2024, 9, 20)),
            stop=wrap_datetime(datetime(2024, 9, 21)),
            data_slices={1: [[14, 18, 21], True, 2, 3, 1, 9, 200]},
        )
        twirled_wrapper = TwirledSliceSpanV2WrapperModel.model_validate({"__value__": twirled_span})

        spans_model = ExecutionSpansModel(spans=[double_wrapper, twirled_wrapper])
        assert len(spans_model.spans) == 2
        assert spans_model.spans[0].type_ == "DoubleSliceSpan"
        assert spans_model.spans[1].type_ == "TwirledSliceSpanV2"

    def test_execution_spans_wrapper_model(self):
        """Test ExecutionSpansWrapperModel."""
        span = DoubleSliceSpanModel(
            start=wrap_datetime(datetime(2024, 8, 20)),
            stop=wrap_datetime(datetime(2024, 8, 21)),
            data_slices={0: [[14], 2, 3, 1, 9]},
        )
        span_wrapper = DoubleSliceSpanWrapperModel.model_validate({"__value__": span})

        spans_model = ExecutionSpansModel(spans=[span_wrapper])
        wrapper = ExecutionSpansWrapperModel.model_validate({"__value__": spans_model})

        assert wrapper.type_ == "ExecutionSpans"
        assert len(wrapper.value_.spans) == 1

    def test_execution_spans_wrapper_serialization(self):
        """Test ExecutionSpansWrapperModel serialization."""
        span = DoubleSliceSpanModel(
            start=wrap_datetime(datetime(2024, 8, 20)),
            stop=wrap_datetime(datetime(2024, 8, 21)),
            data_slices={0: [[14], 2, 3, 1, 9]},
        )
        span_wrapper = DoubleSliceSpanWrapperModel.model_validate({"__value__": span})

        spans_model = ExecutionSpansModel(spans=[span_wrapper])
        wrapper = ExecutionSpansWrapperModel.model_validate({"__value__": spans_model})

        serialized = wrapper.model_dump(by_alias=True)
        assert "__type__" in serialized
        assert "__value__" in serialized
        assert serialized["__type__"] == "ExecutionSpans"
        assert "spans" in serialized["__value__"]
        assert len(serialized["__value__"]["spans"]) == 1


class TestMetadataModels:
    """Test metadata models."""

    def test_execution_metadata_model_with_execution_spans(self):
        """Test ExecutionMetadataModel with proper ExecutionSpans structure."""
        # Create a DoubleSliceSpan
        span = DoubleSliceSpanModel(
            start=wrap_datetime(datetime(2024, 8, 20)),
            stop=wrap_datetime(datetime(2024, 8, 21)),
            data_slices={0: [[14], 2, 3, 1, 9]},
        )
        span_wrapper = DoubleSliceSpanWrapperModel.model_validate({"__value__": span})

        # Create ExecutionSpans
        spans_model = ExecutionSpansModel(spans=[span_wrapper])
        spans_wrapper = ExecutionSpansWrapperModel.model_validate({"__value__": spans_model})

        # Create ExecutionMetadata
        metadata = ExecutionMetadataModel(execution_spans=spans_wrapper)

        assert metadata.execution_spans.type_ == "ExecutionSpans"
        assert len(metadata.execution_spans.value_.spans) == 1
