# This code is a Qiskit project.
#
# (C) Copyright IBM 2025, 2026.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Tests for QPY models."""

from dataclasses import dataclass
from io import BytesIO
from json import JSONDecoder, JSONEncoder
from typing import Any
from zlib import compress

import pytest
from pybase64 import b64encode
from qiskit.circuit import QuantumCircuit
from qiskit.qpy import dump
from samplomatic import ChangeBasis, InjectNoise, Twirl

from ibm_quantum_schemas.common.qpy import (
    CompressedQpyDataModel,
    QpyDataV13ToV17Model,
    QpyModelV13ToV16,
    QpyModelV13ToV17,
    extract_qpy_info,
)


@pytest.mark.parametrize("qpy_version", [15, 16])
@pytest.mark.parametrize("num_circuits", [1, 3])
@pytest.mark.parametrize("compressed", [False, True])
def test_extract_qpy_info(qpy_version, num_circuits, compressed):
    """Test the ``extract_qpy_info`` function."""
    circuit = QuantumCircuit(3)
    circuit.measure_all()

    with BytesIO() as bytes_buf:
        dump([circuit] * num_circuits, bytes_buf, version=qpy_version)
        raw_data = bytes_buf.getvalue()
        if compressed:
            raw_data = compress(raw_data)
        qpy_str = b64encode(raw_data).decode()

    info = extract_qpy_info(qpy_str, compressed)
    assert info.qpy_version == qpy_version
    assert info.num_programs == num_circuits


class TestQpyModelV13ToV16:
    """Tests for ``QpyModelV13ToV16``."""

    @pytest.mark.skip_if_qiskit_too_old_for_qpy
    @pytest.mark.parametrize("qpy_version", [13, 14, 15, 16])
    def test_roundtrip(self, qpy_version):
        """Test that round trips work correctly."""
        circuit = QuantumCircuit(3)
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure_all()

        encoded = QpyModelV13ToV16.from_quantum_circuit(circuit, qpy_version)
        circuit_out = encoded.to_quantum_circuit()

        assert circuit == circuit_out

    @pytest.mark.skip_if_qiskit_too_old_for_qpy
    @pytest.mark.parametrize("qpy_version", [15, 16])
    def test_roundtrip_with_annotations(self, qpy_version):
        """Test that round trips work correctly for circuits with annotated boxes."""
        circuit = QuantumCircuit(3)
        circuit.h(0)
        circuit.cx(0, 1)
        with circuit.box([Twirl(), InjectNoise("ref"), ChangeBasis()]):
            circuit.cx(1, 2)
        circuit.measure_all()

        encoded = QpyModelV13ToV16.from_quantum_circuit(circuit, qpy_version)
        circuit_out = encoded.to_quantum_circuit()

        assert circuit == circuit_out

    @pytest.mark.parametrize("qpy_version", [12, 17])
    def test_unsupported_versions_raise(self, qpy_version):
        """Test that unsupported versions raise."""
        circuit = QuantumCircuit(3)
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure_all()

        with pytest.raises(ValueError):
            QpyModelV13ToV16.from_quantum_circuit(circuit, qpy_version)


class TestQpyModelV13ToV17:
    """Tests for ``QpyModelV13ToV17``."""

    @pytest.mark.skip_if_qiskit_too_old_for_qpy
    @pytest.mark.parametrize("qpy_version", [13, 14, 15, 16, 17])
    def test_roundtrip(self, qpy_version):
        """Test that round trips work correctly."""
        circuit = QuantumCircuit(3)
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure_all()

        encoded = QpyModelV13ToV17.from_quantum_circuit(circuit, qpy_version)
        circuit_out = encoded.to_quantum_circuit()

        assert circuit == circuit_out

    @pytest.mark.skip_if_qiskit_too_old_for_qpy
    @pytest.mark.parametrize("qpy_version", [15, 16, 17])
    def test_roundtrip_with_annotations(self, qpy_version):
        """Test that round trips work correctly for circuits with annotated boxes."""
        circuit = QuantumCircuit(3)
        circuit.h(0)
        circuit.cx(0, 1)
        with circuit.box([Twirl(), InjectNoise("ref"), ChangeBasis()]):
            circuit.cx(1, 2)
        circuit.measure_all()

        encoded = QpyModelV13ToV17.from_quantum_circuit(circuit, qpy_version)
        circuit_out = encoded.to_quantum_circuit()

        assert circuit == circuit_out

    @pytest.mark.parametrize("qpy_version", [12, 18])
    def test_unsupported_versions_raise(self, qpy_version):
        """Test that unsupported versions raise."""
        circuit = QuantumCircuit(3)
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure_all()

        with pytest.raises(ValueError):
            QpyModelV13ToV17.from_quantum_circuit(circuit, qpy_version)


class TestQpyDataV13ToV17Model:
    """Tests for ``QpyModelV13ToV17``."""

    @pytest.mark.skip_if_qiskit_too_old_for_qpy
    @pytest.mark.parametrize("qpy_version", [13, 14, 15, 16, 17])
    def test_roundtrip(self, qpy_version):
        """Test that round trips work correctly."""
        circuit0 = QuantumCircuit(3)
        circuit0.h(0)
        circuit0.cx(0, 1)
        circuit0.measure_all()

        circuit1 = QuantumCircuit(2)
        circuit1.h(0)
        circuit1.measure_all()

        circuits = [circuit0, circuit1]

        encoded = QpyDataV13ToV17Model.from_python(circuits, qpy_version)

        assert encoded.num_programs == 2
        assert encoded.qpy_version == qpy_version

        circuits_out = encoded.to_python()

        assert circuits == circuits_out

    @pytest.mark.skip_if_qiskit_too_old_for_qpy
    @pytest.mark.parametrize("qpy_version", [15, 16, 17])
    def test_roundtrip_with_annotations(self, qpy_version):
        """Test that round trips work correctly for circuits with annotated boxes."""
        circuit = QuantumCircuit(3)
        circuit.h(0)
        circuit.cx(0, 1)
        with circuit.box([Twirl(), InjectNoise("ref"), ChangeBasis()]):
            circuit.cx(1, 2)
        circuit.measure_all()

        encoded = QpyDataV13ToV17Model.from_python([circuit], qpy_version)
        circuits_out = encoded.to_python()

        assert len(circuits_out) == 1
        assert circuit == circuits_out[0]

    @pytest.mark.parametrize("qpy_version", [12, 18])
    def test_unsupported_versions_raise(self, qpy_version):
        """Test that unsupported versions raise."""
        circuit = QuantumCircuit(3)
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure_all()

        with pytest.raises(ValueError):
            QpyDataV13ToV17Model.from_python([circuit], qpy_version)


class TestCompressedQpyDataModel:
    """Tests for ``CompressedQpyDataModel``."""

    @pytest.mark.skip_if_qiskit_too_old_for_qpy
    @pytest.mark.parametrize("qpy_version", [13, 14, 15, 16, 17])
    def test_roundtrip(self, qpy_version):
        """Test that round trips work correctly."""
        circuit0 = QuantumCircuit(3)
        circuit0.h(0)
        circuit0.cx(0, 1)
        circuit0.measure_all()

        circuit1 = QuantumCircuit(2)
        circuit1.h(0)
        circuit1.measure_all()

        circuits = [circuit0, circuit1]

        encoded = CompressedQpyDataModel.from_python(
            circuits,
            qpy_version,
        )

        assert encoded.num_programs == 2
        assert encoded.qpy_version == qpy_version

        circuits_out = encoded.to_python()

        assert circuits == circuits_out

    @pytest.mark.skip_if_qiskit_too_old_for_qpy
    @pytest.mark.parametrize("qpy_version", [15, 16, 17])
    def test_roundtrip_with_annotations(self, qpy_version):
        """Test that round trips work correctly for circuits with annotated boxes."""
        circuit = QuantumCircuit(3)
        circuit.h(0)
        circuit.cx(0, 1)
        with circuit.box([Twirl(), InjectNoise("ref"), ChangeBasis()]):
            circuit.cx(1, 2)
        circuit.measure_all()

        encoded = CompressedQpyDataModel.from_python(
            [circuit],
            qpy_version,
        )
        circuits_out = encoded.to_python()

        assert len(circuits_out) == 1
        assert circuit == circuits_out[0]

    @pytest.mark.parametrize("qpy_version", [12, 18])
    def test_unsupported_versions_raise(self, qpy_version):
        """Test that unsupported versions raise."""
        circuit = QuantumCircuit(3)
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure_all()

        with pytest.raises(ValueError):
            CompressedQpyDataModel.from_python([circuit], qpy_version)

    @pytest.mark.skip_if_qiskit_too_old_for_qpy
    @pytest.mark.parametrize("qpy_version", [13, 14, 15, 16, 17])
    def test_custom_serializers(self, qpy_version):
        """Test that custom serializers work correctly."""

        @dataclass
        class Foo:
            """Custom metadata class for testing."""

            val: int

        class FooEncoder(JSONEncoder):
            """Called to encode `Foo` object."""

            def default(self, obj: Any) -> Any:
                if isinstance(obj, Foo):
                    out_val = {
                        "val": obj.val,
                    }
                    return {"__type__": "Foo", "__value__": out_val}
                return super().default(obj)

        class FooDecoder(JSONDecoder):
            """Called to decode `Foo` object."""

            def __init__(self, *args: Any, **kwargs: Any):
                super().__init__(object_hook=self.object_hook, *args, **kwargs)

            def object_hook(self, obj: Any) -> Any:
                if "__type__" in obj:
                    obj_type = obj["__type__"]
                    obj_val = obj["__value__"]
                    if obj_type == "Foo":
                        return Foo(**obj_val)
                return obj

        metadata = {"experiment_type": Foo(1)}

        circuit0 = QuantumCircuit(3, metadata=metadata)
        circuit0.h(0)
        circuit0.cx(0, 1)
        circuit0.measure_all()

        with pytest.raises(TypeError, match="Object of type Foo is not JSON serializable"):
            encoded = CompressedQpyDataModel.from_python(
                [circuit0],
                qpy_version,
            )

        encoded = CompressedQpyDataModel.from_python(
            [circuit0],
            qpy_version,
            metadata_serializer=FooEncoder,
        )

        assert encoded.num_programs == 1
        assert encoded.qpy_version == qpy_version

        (circuit0_out,) = encoded.to_python(metadata_deserializer=FooDecoder)

        assert circuit0 == circuit0_out
        assert circuit0.metadata == circuit0_out.metadata
