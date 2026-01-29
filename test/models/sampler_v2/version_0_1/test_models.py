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

"""Tests for SamplerV2 0.1 models."""

import datetime

import numpy as np
import pytest
from qiskit.circuit import Parameter, QuantumCircuit

from ibm_quantum_schemas.models.sampler_v2.version_0_1.models import (
    BitArrayModel,
    ChunkPart,
    ChunkSpan,
    DataBinModel,
    DynamicalDecouplingOptionsModel,
    ExecutionOptionsModel,
    MetadataModel,
    OptionsModel,
    ParamsModel,
    PubModel,
    SamplerPubResultModel,
    SamplerResultModel,
    TwirlingOptionsModel,
)
from ibm_quantum_schemas.models.qpy_model import QpyModelV13ToV16
from ibm_quantum_schemas.models.tensor_model import F64TensorModel


def test_bit_array_model():
    """Test BitArrayModel with proper Pydantic validation."""
    # Create a valid BitArray using from_numpy
    original = np.array([0, 1, 2, 3, 255], dtype=np.uint8)
    bit_array = BitArrayModel.from_numpy(original, num_bits=8)
    
    assert bit_array.num_bits == 8
    assert isinstance(bit_array.array, str)
    assert len(bit_array.array) > 0


def test_bitarray_from_numpy():
    """Test BitArrayModel.from_numpy() creates valid model."""
    # Create a simple uint8 array
    original = np.array([0, 1, 2, 3, 255], dtype=np.uint8)
    
    # Create BitArrayModel from numpy array
    model = BitArrayModel.from_numpy(original, num_bits=8)
    
    # Verify the model is valid
    assert model.num_bits == 8
    assert isinstance(model.array, str)
    assert len(model.array) > 0


def test_bitarray_to_numpy():
    """Test BitArrayModel.to_numpy() decodes correctly."""
    # Create a valid encoded BitArray
    original = np.array([42, 100, 200], dtype=np.uint8)
    model = BitArrayModel.from_numpy(original, num_bits=8)
    
    # Decode to numpy array
    array = model.to_numpy()
    
    # Verify it's a uint8 array
    assert array.dtype == np.uint8
    assert isinstance(array, np.ndarray)
    np.testing.assert_array_equal(original, array)


def test_bitarray_roundtrip():
    """Test that from_numpy() and to_numpy() are inverses."""
    # Create various test arrays
    test_arrays = [
        np.array([0, 1, 2, 3, 255], dtype=np.uint8),
        np.array([[0, 1], [2, 3]], dtype=np.uint8),
        np.array([255, 254, 253], dtype=np.uint8),
        np.zeros(10, dtype=np.uint8),
        np.ones(5, dtype=np.uint8) * 128,
    ]
    
    for original in test_arrays:
        # Encode and decode
        model = BitArrayModel.from_numpy(original, num_bits=8)
        recovered = model.to_numpy()
        
        # Verify round-trip preserves data
        np.testing.assert_array_equal(original, recovered)
        assert original.shape == recovered.shape
        assert original.dtype == recovered.dtype


def test_bitarray_from_numpy_wrong_dtype():
    """Test that from_numpy() rejects non-uint8 arrays."""
    # Try with wrong dtypes
    wrong_dtypes = [
        np.array([1, 2, 3], dtype=np.int32),
        np.array([1.0, 2.0, 3.0], dtype=np.float64),
        np.array([True, False], dtype=np.bool_),
    ]
    
    for array in wrong_dtypes:
        with pytest.raises(ValueError, match="uint8"):
            BitArrayModel.from_numpy(array, num_bits=8)


def test_bitarray_invalid_wire_format():
    """Test that invalid wire format raises appropriate errors when decoded."""
    # Invalid base64 - should fail when trying to decode
    bit_array = BitArrayModel(array="not_valid_base64!", num_bits=8)
    with pytest.raises(ValueError, match="Failed to decode BitArray data"):
        bit_array.to_numpy()
    
    # Valid base64 but not zlib compressed - should fail when trying to decode
    import base64
    invalid = base64.standard_b64encode(b"not compressed").decode("utf-8")
    bit_array2 = BitArrayModel(array=invalid, num_bits=8)
    with pytest.raises(ValueError, match="Failed to decode BitArray data"):
        bit_array2.to_numpy()


def test_bitarray_wire_format_compatibility():
    """Test that encoding matches RuntimeEncoder format expectations."""
    # Create a known array
    original = np.array([42, 100, 200], dtype=np.uint8)
    
    # Encode using our method
    model = BitArrayModel.from_numpy(original, num_bits=8)
    
    # Decode and verify
    recovered = model.to_numpy()
    np.testing.assert_array_equal(original, recovered)
    
    # Verify the wire format structure (base64 of zlib of np.save)
    import base64
    import zlib
    import io
    
    # Manually decode to verify structure
    decoded = base64.standard_b64decode(model.array)
    decompressed = zlib.decompress(decoded)
    with io.BytesIO(decompressed) as buff:
        manual_array = np.load(buff, allow_pickle=False)
    
    np.testing.assert_array_equal(original, manual_array)


def test_data_bin_model():
    """Test DataBinModel with proper Pydantic validation."""
    bit_array1 = BitArrayModel.from_numpy(
        np.array([0, 1, 2, 3, 255], dtype=np.uint8),
        num_bits=8
    )
    bit_array2 = BitArrayModel.from_numpy(
        np.array([1, 2, 3, 4], dtype=np.uint8),
        num_bits=4
    )
    
    data_bin = DataBinModel(
        shape=[2, 3],
        field_names=["meas", "alpha"],
        fields={
            "meas": bit_array1,
            "alpha": bit_array2,
        }
    )
    
    assert data_bin.shape == [2, 3]
    assert data_bin.field_names == ["meas", "alpha"]
    assert "meas" in data_bin.fields
    assert isinstance(data_bin.fields["meas"], BitArrayModel)
    assert isinstance(data_bin.fields["alpha"], BitArrayModel)


def test_sampler_pub_result_model():
    """Test SamplerPubResultModel with proper Pydantic validation."""
    bit_array = BitArrayModel.from_numpy(
        np.array([0, 1, 2, 3, 255], dtype=np.uint8),
        num_bits=8
    )
    data_bin = DataBinModel(
        shape=[1, 2],
        field_names=["meas"],
        fields={"meas": bit_array}
    )
    
    pub_result = SamplerPubResultModel(
        data=data_bin,
        metadata={"_pub_shots": 1024, "_meas_type": "classified"}
    )
    
    assert isinstance(pub_result.data, DataBinModel)
    assert pub_result.data == data_bin
    assert pub_result.metadata["_pub_shots"] == 1024
    assert pub_result.metadata["_meas_type"] == "classified"


def test_metadata_models():
    """Test ChunkPart, ChunkSpan, and MetadataModel initialization."""
    chunk_part = ChunkPart(idx_item=0, size=10)
    assert chunk_part.idx_item == 0
    assert chunk_part.size == 10
    
    now = datetime.datetime.now()
    chunk_span = ChunkSpan(
        start=now,
        stop=now + datetime.timedelta(seconds=5.1),
        parts=[chunk_part]
    )
    assert chunk_span.start == now
    assert chunk_span.stop == now + datetime.timedelta(seconds=5.1)
    assert chunk_span.parts == [chunk_part]
    
    metadata = MetadataModel(chunk_timing=[chunk_span])
    assert metadata.chunk_timing == [chunk_span]


def test_sampler_result_model():
    """Test SamplerResultModel with proper Pydantic validation."""
    bit_array = BitArrayModel.from_numpy(
        np.array([0, 1, 2, 3, 255], dtype=np.uint8),
        num_bits=8
    )
    data_bin = DataBinModel(
        shape=[1, 2],
        field_names=["meas"],
        fields={"meas": bit_array}
    )
    pub_result = SamplerPubResultModel(
        data=data_bin,
        metadata={}
    )
    
    now = datetime.datetime.now()
    chunk_span = ChunkSpan(
        start=now,
        stop=now + datetime.timedelta(seconds=5.1),
        parts=[ChunkPart(idx_item=0, size=2)]
    )
    
    result = SamplerResultModel(
        pub_results=[pub_result],
        metadata={"chunk_timing": [chunk_span.model_dump()]}
    )
    
    assert result.schema_version == "v0.1"
    assert len(result.pub_results) == 1
    assert isinstance(result.pub_results[0], SamplerPubResultModel)
    assert result.pub_results[0] == pub_result


@pytest.mark.parametrize("qpy_version", [13, 14, 15, 16])
def test_params_model_initialization(qpy_version):
    """Test ParamsModel initialization with tuple PUBs."""
    circuit = QuantumCircuit(2)
    circuit.rx(Parameter("theta"), 0)
    circuit.cx(0, 1)
    circuit.measure_all()
    
    # PubModel is a tuple: (circuit, parameter_values, shots)
    pub: PubModel = (
        QpyModelV13ToV16.from_quantum_circuit(circuit, qpy_version),
        F64TensorModel.from_numpy(np.array([0.5], dtype=np.float64)),
        1024
    )
    
    options = OptionsModel(
        default_shots=4096,
        execution=ExecutionOptionsModel(
            init_qubits=True,
            meas_type="classified"
        ),
        twirling=TwirlingOptionsModel(enable_gates=True),
        dynamical_decoupling=DynamicalDecouplingOptionsModel(enable=True)
    )
    
    params = ParamsModel(pubs=[pub], options=options)
    
    assert params.schema_version == "v0.1"
    assert len(params.pubs) == 1
    assert params.pubs[0] == pub
    assert params.options == options


def test_options_model_defaults():
    """Test OptionsModel default values with new structure."""
    options = OptionsModel()
    
    assert options.default_shots == 4096
    assert options.execution.init_qubits is True
    assert options.execution.rep_delay is None
    assert options.execution.meas_type == "classified"
    assert options.twirling.enable_gates is False
    assert options.twirling.enable_measure is False
    assert options.dynamical_decoupling.enable is False


def test_options_model_meas_type_twirling_validation():
    """Test that kerneled meas_type and measurement twirling are incompatible."""
    with pytest.raises(ValueError, match="Kerneled measurement return and measurement twirling"):
        OptionsModel(
            execution=ExecutionOptionsModel(meas_type="kerneled"),
            twirling=TwirlingOptionsModel(enable_measure=True)
        )


def test_pub_model_as_tuple():
    """Test PubModel is a tuple type."""
    circuit = QuantumCircuit(2)
    circuit.rx(Parameter("theta"), 0)
    circuit.cx(0, 1)
    
    # PubModel is a tuple: (circuit, parameter_values, shots)
    pub: PubModel = (
        QpyModelV13ToV16.from_quantum_circuit(circuit, 16),
        F64TensorModel.from_numpy(np.array([0.5], dtype=np.float64)),
        1024
    )
    
    assert isinstance(pub, tuple)
    assert len(pub) == 3
    assert isinstance(pub[0], QpyModelV13ToV16)
    assert isinstance(pub[1], F64TensorModel)
    assert pub[2] == 1024


def test_pub_model_optional_shots():
    """Test PubModel tuple with None shots."""
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    
    # Shots can be None
    pub: PubModel = (
        QpyModelV13ToV16.from_quantum_circuit(circuit, 16),
        F64TensorModel.from_numpy(np.array([], dtype=np.float64)),
        None
    )
    
    assert isinstance(pub, tuple)
    assert pub[2] is None


def test_result_models_validation():
    """Test that result models provide proper Pydantic validation."""
    # Test BitArrayModel validation - num_bits must be int
    with pytest.raises(ValueError):
        BitArrayModel(array="eJyb7BfqGxDJyFDGUK2eklqcXKRupaBuk2ahYGBgYAIA5OwGxA==", num_bits="not_an_int")  # type: ignore
    
    # Test BitArrayModel validation - array must be str
    with pytest.raises(ValueError):
        BitArrayModel(array=[[1, 2]], num_bits=8)  # type: ignore
    
    # Test DataBinModel validation
    with pytest.raises(ValueError):
        DataBinModel(
            shape="not_a_list",  # type: ignore
            field_names=["meas"],
            fields={}
        )
    
    # Test SamplerResultModel validation
    with pytest.raises(ValueError):
        SamplerResultModel(
            pub_results="not_a_list",  # type: ignore
            metadata={}
        )


def test_model_serialization():
    """Test that models can be serialized and deserialized."""
    # Create a valid BitArray
    original_array = np.array([0, 1, 2, 3, 255], dtype=np.uint8)
    bit_array = BitArrayModel.from_numpy(original_array, num_bits=8)
    
    # Serialize
    serialized = bit_array.model_dump()
    assert "array" in serialized
    assert serialized["num_bits"] == 8
    
    # Deserialize
    deserialized = BitArrayModel(**serialized)
    assert deserialized.array == bit_array.array
    assert deserialized.num_bits == 8
    
    # Verify round-trip through serialization
    recovered = deserialized.to_numpy()
    np.testing.assert_array_equal(original_array, recovered)


def test_runtime_encoder_compatibility():
    """Test that models match RuntimeEncoder's __value__ structure."""
    original_array = np.array([42, 100, 200], dtype=np.uint8)
    bit_array = BitArrayModel.from_numpy(original_array, num_bits=8)
    bit_array_value = bit_array.model_dump()
    
    # Verify structure
    assert "array" in bit_array_value
    assert "num_bits" in bit_array_value
    assert bit_array_value["num_bits"] == 8
    
    # Verify can be reconstructed
    reconstructed = BitArrayModel(**bit_array_value)
    assert reconstructed.model_dump() == bit_array_value
    
    data_bin_value = {
        "shape": [1, 2],
        "field_names": ["meas"],
        "fields": {"meas": bit_array}
    }
    data_bin = DataBinModel(**data_bin_value)
    assert data_bin.shape == [1, 2]
    assert data_bin.field_names == ["meas"]
    assert isinstance(data_bin.fields["meas"], BitArrayModel)
    
    pub_result_value = {"data": data_bin, "metadata": {"test": "value"}}
    pub_result = SamplerPubResultModel(**pub_result_value)
    assert isinstance(pub_result.data, DataBinModel)
    assert pub_result.data == data_bin
    assert pub_result.metadata == {"test": "value"}
    
    result_value = {"pub_results": [pub_result], "metadata": {}}
    result = SamplerResultModel(**result_value)
    assert len(result.pub_results) == 1
    assert isinstance(result.pub_results[0], SamplerPubResultModel)
    assert result.pub_results[0] == pub_result