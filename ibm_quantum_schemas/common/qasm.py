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

import qiskit.qasm3 as qasm3
from pydantic import BaseModel, PrivateAttr
from qiskit import QuantumCircuit
from typing_extensions import Self

from ibm_quantum_schemas.common.annotation_serializer import AnnotationSerializer

ANNOTATION_FACTORIES = {"samplomatic": AnnotationSerializer()}

T = TypeVar("T", bound=QuantumCircuit)


class OpenQasm3DataModel(BaseModel, Generic[T]):
    """OpenQASM3-encoded Qiskit objects."""

    data: list[str]
    """Data of the OpenQASM3 serialization of some Qiskit objects."""

    num_qubits: list[int]
    """The number of qubits for each Qiskit object."""

    _python_data: list[T] = PrivateAttr()

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
            self._python_data = [
                qasm3.loads(circ, num_qubits=n_q, annotation_handlers=ANNOTATION_FACTORIES)
                for circ, n_q in zip(self.data, self.num_qubits)
            ]
        return self._python_data

    @classmethod
    def from_python(cls, data: list[T]) -> Self:
        """Create a model instance from Python data of the correct type.

        The returned instance owns a reference to the provided data. This instance may be
        returned by :meth:`~to_python` depending on the value of ``use_cached``.
        Users of this class are responsible for managing cached instances of the data and
        possible side-effects of their mutations.

        Args:
            data: The data to base64 encode in the new model instance.

        Returns:
            A new model instance.
        """
        encoded_data = [qasm3.dumps(i, annotation_handlers=ANNOTATION_FACTORIES) for i in data]
        num_qubits = [i.num_qubits for i in data]
        obj = cls(data=encoded_data, num_qubits=num_qubits)
        obj._python_data = data  # noqa: SLF001
        return obj
