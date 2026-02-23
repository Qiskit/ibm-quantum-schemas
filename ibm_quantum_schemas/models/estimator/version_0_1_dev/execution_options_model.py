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

"""Execution Options Model"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ExecutionOptionsV2Model(BaseModel):
    """Execution options for V2 primitives."""

    model_config = ConfigDict(extra="forbid")

    init_qubits: bool = True
    """Whether to reset the qubits to the ground state for each shot."""

    rep_delay: float | None = None
    """The repetition delay. This is the delay between a measurement and
    the subsequent quantum circuit. This is only supported on backends that have
    ``backend.dynamic_reprate_enabled=True``. It must be from the
    range supplied by ``backend.rep_delay_range``.
    Default is given by ``backend.default_rep_delay``.
    """
