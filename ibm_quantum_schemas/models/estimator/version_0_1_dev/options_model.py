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

"""Estimator Options Model"""

from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from .dynamical_decoupling_options_model import DynamicalDecouplingOptionsModel
from .execution_options_model import ExecutionOptionsV2Model
from .resilience_options_model import ResilienceOptionsModel
from .twirling_options_model import TwirlingOptionsModel
from .simulator_options_model import SimulatorOptionsModel


class OptionsModel(BaseModel):
    """Options for the Estimator."""

    model_config = ConfigDict(extra="forbid")

    default_precision: Annotated[float, Field(ge=0)] = 0.015625
    """The default precision to use for any PUB or ``run()``
    call that does not specify one.
    Each Estimator PUB can specify its own precision. If the ``run()`` method
    is given a precision, then that value is used for all PUBs in the ``run()``
    call that do not specify their own.
    """

    default_shots: Annotated[int, Field(ge=1)] | None = None
    """The total number of shots to use per circuit per configuration.

    .. note::
        If set, this value overrides :attr:`~default_precision`.

    A configuration is a combination of a specific parameter value binding set and a
    physical measurement basis. A physical measurement basis groups together some
    collection of qubit-wise commuting observables for some specific circuit/parameter
    value set to create a single measurement with basis rotations that is inserted into
    hardware executions.

    If twirling is enabled, the value of this option will be divided over circuit
    randomizations, with a smaller number of shots per randomization. See the
    :attr:`~twirling` options.
    """

    seed_estimator: Annotated[int, Field(ge=0)] | None = None
    """Seed used to control sampling."""

    dynamical_decoupling: DynamicalDecouplingOptionsModel = Field(
        default_factory=DynamicalDecouplingOptionsModel
    )
    """Dynamical decoupling options.
    
    See :class:`DynamicalDecouplingOptionsModel` for all available options.
    """

    resilience: ResilienceOptionsModel = Field(default_factory=ResilienceOptionsModel)
    """Advanced resilience options to fine-tune the resilience strategy.
    
    See :class:`ResilienceOptionsModel` for all available options.
    """

    execution: ExecutionOptionsV2Model = Field(default_factory=ExecutionOptionsV2Model)
    """Execution time options.
    
    See :class:`ExecutionOptionsV2Model` for all available options.
    """

    twirling: TwirlingOptionsModel = Field(default_factory=TwirlingOptionsModel)
    """Pauli twirling options.
    
    See :class:`TwirlingOptionsModel` for all available options.
    """

    simulator: SimulatorOptionsModel = Field(default_factory=SimulatorOptionsModel)
    """Simulator options.
    
    See :class:`SimulatorOptionsModel` for all available options.
    """

    experimental: dict = {}
    """Experimental options. These options are subject to change without notification, and
    stability is not guaranteed.
    """
