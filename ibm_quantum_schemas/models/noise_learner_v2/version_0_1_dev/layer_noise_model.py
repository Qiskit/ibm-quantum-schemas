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


class PauliLindbladErrorModel(BaseModel):
    """A Pauli Lindblad error channel for a layer.

    Encoded via RuntimeEncoder using the _json method, which adds __type__, __module__,
    __class__, and __value__ fields.
    """

    type_: Literal["_json"] = Field(default="_json", alias="__type__")
    """The type marker used by RuntimeEncoder for objects with _json method."""

    module_: Literal["qiskit_ibm_runtime.utils.noise_learner_result"] = Field(
        default="qiskit_ibm_runtime.utils.noise_learner_result", alias="__module__"
    )
    """The module name of the original class (qiskit_ibm_runtime.utils.noise_learner_result)."""

    class_: Literal["PauliLindbladError"] = Field(default="PauliLindbladError", alias="__class__")
    """The class name of the original object (PauliLindbladError)."""

    value_: "PauliLindbladErrorValueModel" = Field(alias="__value__")
    """The value returned by the _json method."""


class PauliListSettingsModel(BaseModel):
    """A PauliList encoded via RuntimeEncoder's settings handler.

    PauliList objects have a 'settings' property that returns {"data": self.to_labels()},
    which converts the PauliList to a list of Pauli string labels. The RuntimeEncoder
    detects this and wraps it with type information.
    """

    type_: Literal["settings"] = Field(default="settings", alias="__type__")
    """The type marker used by RuntimeEncoder for objects with settings property."""

    module_: Literal["qiskit.quantum_info.operators.symplectic.pauli_list"] = Field(
        default="qiskit.quantum_info.operators.symplectic.pauli_list", alias="__module__"
    )
    """The module name (qiskit.quantum_info.operators.symplectic.pauli_list)."""

    class_: Literal["PauliList"] = Field(default="PauliList", alias="__class__")
    """The class name (PauliList)."""

    value_: "PauliListSettingsValueModel" = Field(alias="__value__")
    """The value from the settings property."""


class PauliListSettingsValueModel(BaseModel):
    """The value content from PauliList.settings property."""

    data: list[str]
    """List of Pauli string labels.

    Each string is a Pauli operator label (e.g., "IXYZ", "ZZII") representing
    the Pauli generators. The strings use the standard Pauli notation where
    I=identity, X/Y/Z are the Pauli matrices, and optional phase prefixes
    (+, -, i, -i) indicate the global phase.
    """


class PauliLindbladErrorValueModel(BaseModel):
    """The value content of a PauliLindbladError from its _json method."""

    generators: PauliListSettingsModel
    """The Pauli Lindblad generators encoded as a settings-wrapped PauliList.

    This is a PauliList object from qiskit.quantum_info that gets serialized
    through RuntimeEncoder's settings handler. The PauliList contains the
    Pauli operators that generate the error channel.
    """

    rates: list[float]
    """The rates associated with each Pauli Lindblad generator.

    Must have the same length as the generators list. Each rate corresponds to
    the strength of the corresponding generator in the error channel.
    """


class LayerNoiseModel(BaseModel):
    """Results for a single noise learner v2 layer.

    Encoded via RuntimeEncoder using the _json method, which adds __type__, __module__,
    __class__, and __value__ fields.
    """

    type_: Literal["_json"] = Field(default="_json", alias="__type__")
    """The type marker used by RuntimeEncoder for objects with _json method."""

    module_: Literal["qiskit_ibm_runtime.utils.noise_learner_result"] = Field(
        default="qiskit_ibm_runtime.utils.noise_learner_result", alias="__module__"
    )
    """The module name of the original class (qiskit_ibm_runtime.utils.noise_learner_result)."""

    class_: Literal["LayerError"] = Field(default="LayerError", alias="__class__")
    """The class name of the original object (LayerError)."""

    value_: "LayerNoiseValueModel" = Field(alias="__value__")
    """The value returned by the _json method."""


class LayerNoiseValueModel(BaseModel):
    """The value content of a LayerError from its _json method."""

    circuit: CircuitQpyModelV13to17
    """The circuit representing this layer.

    This is the quantum circuit whose noise has been learned, encoded in QPY format.
    """

    qubits: list[int]
    """The physical qubit labels for this layer.

    Maps the circuit qubits to physical backend qubits.
    """

    error: PauliLindbladErrorModel | None = None
    """The learned Pauli Lindblad error channel for this layer.

    If None, the error channel is either unknown or explicitly disabled for this layer.
    """
