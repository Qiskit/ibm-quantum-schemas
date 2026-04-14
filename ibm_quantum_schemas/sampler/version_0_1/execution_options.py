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

"""Sampler Execution Options Model"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Field


class SamplerExecutionOptionsModel(BaseModel):
    """Execution options for Sampler V2."""

    init_qubits: bool = True
    """Whether to reset the qubits to the ground state for each shot."""

    rep_delay: Annotated[float, Field(ge=0)] | None = None
    """The repetition delay.

    This is the delay between a measurement and the subsequent quantum circuit. This is only
    supported on backends that have ``backend.dynamic_reprate_enabled=True``. It must be from the
    range supplied by ``backend.rep_delay_range``.

    Default is ``None``, in which case the server assigns ``backend.default_rep_delay``.
    """

    meas_type: Literal["classified", "kerneled", "avg_kerneled"] = "classified"
    """How to process and return measurement results.

    This option sets the return type of all classical registers in all
    SamplerPubResults. If a sampler pub with shape ``pub_shape`` has a circuit that
    contains a classical register with size ``creg_size``, then the returned data
    associated with this register will have one of the following formats depending
    on the value of this option.

    * ``"classified"``: A BitArray of shape ``pub_shape`` over ``num_shots`` with a
      number of bits equal to ``creg_size``.

    * ``"kerneled"``: A complex NumPy array of shape ``(*pub_shape, num_shots, creg_size)``,
      where each entry represents an IQ data point (resulting from kerneling the measurement
      trace) in arbitrary units.

    * ``"avg_kerneled"``: A complex NumPy array of shape ``(*pub_shape, creg_size)``, where
      each entry represents an IQ data point (resulting from kerneling the measurement trace
      and averaging over shots) in arbitrary units. This option is equivalent to selecting
      ``"kerneled"`` and then averaging over the shots axis, but requires less data bandwidth.
    """
