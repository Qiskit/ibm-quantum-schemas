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

"""All models needed for LayerNoiseModel"""

from typing import Literal

from pydantic import BaseModel, Field

from .circuit_qpy_model_v13_to_v17 import CircuitQpyModelV13to17


class PauliListModel(BaseModel):
    """Represents a PauliList"""

    data: list[str]
    """List of Pauli string labels.

    Each string is a Pauli operator label (e.g., "IXYZ", "ZZII") representing
    the Pauli generators. The strings use the standard Pauli notation where
    I=identity, X/Y/Z are the Pauli matrices, and optional phase prefixes
    (+, -, i, -i) indicate the global phase.
    """


class PauliListWrapperModel(BaseModel):
    """A wrapper around PauliListModel adding redundant type information."""

    type_: Literal["settings"] = Field(default="settings", alias="__type__")
    """Redundant type information."""

    module_: Literal["qiskit.quantum_info.operators.symplectic.pauli_list"] = Field(
        default="qiskit.quantum_info.operators.symplectic.pauli_list", alias="__module__"
    )
    """Redundant type information."""

    class_: Literal["PauliList"] = Field(default="PauliList", alias="__class__")
    """Redundant type information."""

    value_: PauliListModel = Field(alias="__value__")
    """The actual data."""


class NdarrayWrapperModel(BaseModel):
    """A wrapper around ndarray data adding redundant type information."""

    type_: Literal["ndarray"] = Field(default="ndarray", alias="__type__")
    """Redundant type information."""

    value_: str = Field(alias="__value__")
    """The actual data: Base64-encoded, zlib compressed numpy binary format of an ndarray."""


class PauliLindbladErrorModel(BaseModel):
    """The Pauli Lindblad error data."""

    generators: PauliListWrapperModel
    """The Pauli Lindblad generators as a PauliList.

    Contains the Pauli operators that generate the error channel.
    """

    rates: NdarrayWrapperModel
    """The rates associated with each Pauli Lindblad generator.

    A NumPy ndarray containing float values with the same length as the generators list.
    Each rate corresponds to the strength of the corresponding generator in the error channel.
    """


class PauliLindbladErrorWrapperModel(BaseModel):
    """A wrapper around PauliLindbladErrorModel adding redundant type information."""

    type_: Literal["_json"] = Field(default="_json", alias="__type__")
    """Redundant type information."""

    module_: Literal["qiskit_ibm_runtime.utils.noise_learner_result"] = Field(
        default="qiskit_ibm_runtime.utils.noise_learner_result", alias="__module__"
    )
    """Redundant type information."""

    class_: Literal["PauliLindbladError"] = Field(default="PauliLindbladError", alias="__class__")
    """Redundant type information."""

    value_: PauliLindbladErrorModel = Field(alias="__value__")
    """The actual data."""


class LayerNoiseModel(BaseModel):
    """The error data."""

    circuit: CircuitQpyModelV13to17
    """The quantum circuit whose noise has been learned, encoded in QPY format."""

    qubits: list[int]
    """The physical qubit labels for this layer.

    Maps the circuit qubits to physical backend qubits.
    """

    error: PauliLindbladErrorWrapperModel | None = None
    """The learned Pauli Lindblad error channel for this layer.

    If None, the error channel is either unknown or explicitly disabled for this layer.
    """


class LayerNoiseWrapperModel(BaseModel):
    """A wrapper around LayerNoiseModel adding redundant type information."""

    type_: Literal["_json"] = Field(default="_json", alias="__type__")
    """Redundant type information."""

    module_: Literal["qiskit_ibm_runtime.utils.noise_learner_result"] = Field(
        default="qiskit_ibm_runtime.utils.noise_learner_result", alias="__module__"
    )
    """Redundant type information."""

    class_: Literal["LayerError"] = Field(default="LayerError", alias="__class__")
    """Redundant type information."""

    value_: LayerNoiseModel = Field(alias="__value__")
    """The actual data."""
