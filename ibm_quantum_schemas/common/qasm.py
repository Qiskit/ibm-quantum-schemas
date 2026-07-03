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

"""OpenQASM3Model"""

from typing import Generic, TypeVar
from uuid import UUID

import qiskit.qasm3 as qasm3
from pydantic import BaseModel, PrivateAttr
from qiskit.circuit import Parameter, QuantumCircuit
from typing_extensions import Self

from ibm_quantum_schemas.common.annotation_serializer import OpenQASM3AnnotationSerializer

ANNOTATION_FACTORIES = {"samplomatic": OpenQASM3AnnotationSerializer()}

T = TypeVar("T", bound=QuantumCircuit)


class OpenQasm3DataModel(BaseModel, Generic[T]):
    """OpenQASM3-encoded objects."""

    data: list[str]
    """A list of OpenQASM3 serialized programs."""

    _uuids: list[list[UUID]] = PrivateAttr()
    """Parameter UUIDs cached from Python to ensure parameters match the original encoding."""

    _python_data: list[T] = PrivateAttr()

    @property
    def num_programs(self) -> int:
        """The number of distinct elements in the Python encoding."""
        return len(self.data)

    def to_python(self, use_cached: bool = False) -> list[T]:
        """Return a Python representation of the encoded data in the model.

        When ``use_cached`` is false, or when no cached version exists, :attr:`~data` is
        decoded and loaded into a new Python instance. Users of this class are responsible for
        managing cached instances of the Python data and possible side-effects of their mutations.

        Args:
            use_cached: Whether to return the cached instance (if it exists).

        Returns:
            Python data.
        """
        if not use_cached or not hasattr(self, "_python_data"):
            data = []
            for idx, qasm_circ in enumerate(self.data):
                python_circ = qasm3.loads(qasm_circ, annotation_handlers=ANNOTATION_FACTORIES)
                if hasattr(self, "_uuids"):
                    # OpenQASM3.0 workaround to ensure parameters match the original encoding
                    replacements = {
                        param: Parameter(name=param.name, uuid=uuid)
                        for param, uuid in zip(python_circ.parameters, self._uuids[idx])
                    }
                    python_circ = python_circ.assign_parameters(replacements)
                data.append(python_circ)
            self._python_data = data

        return self._python_data

    @classmethod
    def from_python(cls, data: list[T]) -> Self:
        """Create a model instance from Python data of the correct type.

        The returned instance owns a reference to the provided data. This instance may be
        returned by :meth:`~to_python` depending on the value of ``use_cached``.
        Users of this class are responsible for managing cached instances of the data and
        possible side-effects of their mutations.

        Args:
            data: The data to string encode in the new model instance.

        Returns:
            A new model instance.
        """
        qasm_exported = qasm3.Exporter(annotation_handlers=ANNOTATION_FACTORIES)
        encoded_data = [qasm_exported.dumps(i) for i in data]
        obj = cls(data=encoded_data)
        obj._python_data = data  # noqa: SLF001
        uuids = [[p.uuid for p in i.parameters] for i in data]
        obj._uuids = uuids  # noqa: SLF001
        return obj
