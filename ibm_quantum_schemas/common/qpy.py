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

"""QpyModel"""

import struct
from dataclasses import dataclass
from io import BytesIO
from typing import Generic, TypeVar

from pybase64 import b64decode, b64encode
from pydantic import BaseModel, Field, PrivateAttr, model_validator
from qiskit import QuantumCircuit
from qiskit.qpy import QPY_VERSION, dump, load
from qiskit.qpy.formats import FILE_HEADER_V10, FILE_HEADER_V10_PACK, FILE_HEADER_V10_SIZE
from qiskit.qpy.interface import QPY_SUPPORTED_TYPES
from typing_extensions import Self

from ibm_quantum_schemas.common.annotation_serializer import AnnotationSerializer
from ibm_quantum_schemas.common.base64_reader import Base64Reader

ANNOTATION_FACTORIES = {"samplomatic": AnnotationSerializer}

T = TypeVar("T", bound=QPY_SUPPORTED_TYPES)


@dataclass(frozen=True, slots=True)
class QpyInfo:
    """Information about the contents of a QPY file."""

    qpy_version: int
    """The QPY verson."""

    num_programs: int
    """The number of independent components inside the file."""


def extract_qpy_info(qpy_b64: str) -> QpyInfo:
    """Return information about a QPY binary stream.

    Args:
        qpy_b64: A QPY file encoded as a base64 string.

    Returns:
        Information about the QPY content.
    """
    with Base64Reader(qpy_b64) as bytes_obj:
        header = FILE_HEADER_V10._make(
            struct.unpack(
                FILE_HEADER_V10_PACK,
                bytes_obj.read(FILE_HEADER_V10_SIZE),
            )
        )
    return QpyInfo(header.qpy_version, header.num_programs)


class QpyDataModel(BaseModel, Generic[T]):
    """QPY-encoded Qiskit objects."""

    b64_data: str
    """Base-64 encoded data of the QPY serialization of some Qiskit objects."""

    qpy_version: int = Field(ge=10)
    """The QPY encoding version."""

    num_programs: int = Field(ge=1)
    """The number of distinct elements in the Python encoding."""

    _python_data: list[T] = PrivateAttr()

    @model_validator(mode="after")
    def cross_validate_qpy_info(self):
        """Check that the encoded qpy information matches expectations."""
        qpy_info = extract_qpy_info(self.b64_data)
        if qpy_info.qpy_version != self.qpy_version:
            raise ValueError(
                f"The qpy_version is {self.qpy_version} but the encoded QPY "
                f"version is {qpy_info.qpy_version}."
            )
        if qpy_info.num_programs != self.num_programs:
            raise ValueError(
                f"num_programs={self.num_programs}, but the encoded QPY "
                f"has {qpy_info.num_programs} elements"
            )
        return self

    def to_python(self, use_cached: bool = False) -> list[T]:
        """Return a Python representation of the encoded data in the model.

        When ``use_cached`` is false, or when no cached version exists, :attr:`~b64_data` is
        decoded and loaded into a new Python instance. Users of this class are responsible for
        managing cached instances of the Python data and possible side-effects of their mutations.

        Args:
            use_cached: Whether to return the cached instance (if it exists).

        Returns:
            Python data.
        """
        if not use_cached or not hasattr(self, "_python_data"):
            with BytesIO(b64decode(self.b64_data)) as bytes_obj:
                self._python_data = load(bytes_obj, annotation_factories=ANNOTATION_FACTORIES)

        return self._python_data

    @classmethod
    def from_python(cls, data: list[T], qpy_version: int = QPY_VERSION) -> Self:
        """Create a model instance from Python data of the correct type.

        The returned instance owns a reference to the provided data. This instance may be
        returned by :meth:`~to_python` depending on the value of ``use_cached``.
        Users of this class are responsible for managing cached instances of the data and
        possible side-effects of their mutations.

        Args:
            data: The data to base64 encode in the new model instance.
            qpy_version: The QPY version to encode with.

        Returns:
            A new model instance.
        """
        with BytesIO() as bytes_obj:
            dump(data, bytes_obj, version=qpy_version, annotation_factories=ANNOTATION_FACTORIES)
            b64_data = b64encode(bytes_obj.getvalue()).decode()

        obj = cls(b64_data=b64_data, qpy_version=qpy_version, num_programs=len(data))
        obj._python_data = data  # noqa: SLF001
        return obj


# This class does not use/inherit QpyDataModel for historical reasons. Since some program models
# depend on it, we leave it as-is.
class QpyModel(BaseModel):
    """A QPY-encoded quantum circuit."""

    circuit_b64: str
    """Base-64 encoded data of the QPY serialization of a single quantum circuit."""

    qpy_version: int = Field(ge=10)
    """The QPY encoding version."""

    _circuit: QuantumCircuit = PrivateAttr()

    @model_validator(mode="after")
    def cross_validate_qpy_version(self):
        """Check that the reported version matches the encoded version."""
        qpy_info = extract_qpy_info(self.circuit_b64)
        if qpy_info.qpy_version != self.qpy_version:
            raise ValueError(
                f"The qpy_version is {self.qpy_version} but the encoded QPY "
                f"version is {qpy_info.qpy_version}."
            )
        if qpy_info.num_programs != 1:
            raise ValueError(
                f"Expected exactly one encoded quantum circuit, received {qpy_info.num_programs}"
            )
        return self

    def to_quantum_circuit(self, use_cached: bool = False) -> QuantumCircuit:
        """Return a decoded quantum circuit instance.

        When ``use_cached`` is false, or when no cached version exists, :attr:`~circuit_b64` is
        decoded and loaded into a new instance. Users of this class are responsible for managing
        cached instances of the circuit and possible side-effects of their mutations.

        Args:
            use_cached: Whether to return the cached instance (if it exists).

        Returns:
            A quantum circuit.
        """
        if not use_cached or not hasattr(self, "_circuit"):
            with BytesIO(b64decode(self.circuit_b64)) as bytes_obj:
                self._circuit = load(bytes_obj, annotation_factories=ANNOTATION_FACTORIES)[0]

        return self._circuit

    @classmethod
    def from_quantum_circuit(cls, circuit: QuantumCircuit, qpy_version: int = QPY_VERSION) -> Self:
        """Create a model instance from a quantum circuit.

        The returned instance owns a reference to the provided circuit. This instance may be
        returned by :meth:`~to_quantum_circuit` depending on the value of ``use_cached``.
        Users of this class are responsible for managing cached instances of the circuit and
        possible side-effects of their mutations.

        Args:
            circuit: The circuit to encode into the model.
            qpy_version: The QPY version to encode with.

        Returns:
            A new model instance.
        """
        with BytesIO() as bytes_obj:
            dump(circuit, bytes_obj, version=qpy_version, annotation_factories=ANNOTATION_FACTORIES)
            circuit_b64 = b64encode(bytes_obj.getvalue()).decode()

        obj = cls(circuit_b64=circuit_b64, qpy_version=qpy_version)
        obj._circuit = circuit  # noqa: SLF001
        return obj


class QpyModelV13ToV16(QpyModel):
    """QPY encoded circuits with restricted version range."""

    qpy_version: int = Field(ge=13, le=16)


class QpyModelV13ToV17(QpyModel):
    """QPY encoded circuits with restricted version range."""

    qpy_version: int = Field(ge=13, le=17)


class QpyDataV13ToV17Model(QpyDataModel[T], Generic[T]):
    """QPY encoded circuit list with restricted version range."""

    qpy_version: int = Field(ge=13, le=17)
