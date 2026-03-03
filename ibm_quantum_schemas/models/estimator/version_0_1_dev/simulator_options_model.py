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

"""All Models around OptionsModel"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, conlist


class NoiseModel(BaseModel):
    """A wrapper around Noise model data for the simulator."""

    type_: Literal["NoiseModel"] = Field(default="NoiseModel", alias="__type__")
    """Redundant type information."""

    value_: dict = Field(alias="__value__")
    """The actual data: qiskit-aer dict format for the NoiseModel."""


class SimulatorOptionsModel(BaseModel):
    """Simulator options for the noise learner."""

    model_config = ConfigDict(extra="forbid")

    noise_model: NoiseModel | None = None
    """Noise model for the simulator.

    This option is only supported in local testing mode.
    Default: ``None``.
    """

    seed_simulator: int | None = None
    """Random seed to control sampling.

    Default: ``None``.
    """

    coupling_map: (
        conlist(conlist(int, min_length=2, max_length=2)) | None  # type: ignore[valid-type]
    ) = None
    """Directed coupling map to target in mapping.

    If the coupling map is symmetric, both directions need to be specified.
    Each entry in the list specifies a directed two-qubit interaction,
    e.g: ``[[0, 1], [0, 3], [1, 2], [1, 5], [2, 5], [4, 1], [5, 3]]``.

    Default: ``None``, which implies no connectivity constraints.
    """

    basis_gates: list[str] | None = None
    """List of basis gate names to unroll to.

    For example, ``['u1', 'u2', 'u3', 'cx']``. Unrolling is not done if not set.

    Default: ``None``, implying all basis gates supported by the simulator.
    """
