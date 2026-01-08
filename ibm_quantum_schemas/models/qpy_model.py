# This code is a Qiskit project.
#
# (C) Copyright IBM 2025.
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
from io import BytesIO

import pybase64
from pydantic import BaseModel, Field, PrivateAttr, model_validator
from qiskit import QuantumCircuit
from qiskit.qpy import QPY_VERSION, dump, load
from qiskit.qpy.formats import FILE_HEADER_V10, FILE_HEADER_V10_PACK, FILE_HEADER_V10_SIZE

from .annotation_serializer import AnnotationSerializer

ANNOTATION_FACTORIES = {"samplomatic": AnnotationSerializer}


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
        with BytesIO(pybase64.b64decode(self.circuit_b64)) as bytes_obj:
            header = FILE_HEADER_V10._make(
                struct.unpack(
                    FILE_HEADER_V10_PACK,
                    bytes_obj.read(FILE_HEADER_V10_SIZE),
                )
            )
            if header.qpy_version != self.qpy_version:
                raise ValueError(
                    f"The qpy_version is {self.qpy_version} but the encoded QPY "
                    f"version is {header.qpy_version}."
                )
            if header.num_programs != 1:
                raise ValueError(
                    f"Expected exactly one encoded quantum circuit, received {header.num_programs}"
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
            with BytesIO(pybase64.b64decode(self.circuit_b64)) as bytes_obj:
                self._circuit = load(bytes_obj, annotation_factories=ANNOTATION_FACTORIES)[0]

        return self._circuit

    @classmethod
    def from_quantum_circuit(cls, circuit: QuantumCircuit, qpy_version: int = QPY_VERSION):
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
            circuit_b64 = pybase64.b64encode(bytes_obj.getvalue()).decode()

        obj = cls(circuit_b64=circuit_b64, qpy_version=qpy_version)
        obj._circuit = circuit  # noqa: SLF001
        return obj


class QpyModelV13ToV16(QpyModel):
    """QPY encoded circuits with restricted version range."""

    qpy_version: int = Field(ge=13, le=16)


class QpyModelV13ToV17(QpyModel):
    """QPY encoded circuits with restricted version range."""

    qpy_version: int = Field(ge=13, le=17)
