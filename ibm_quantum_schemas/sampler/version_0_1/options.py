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

"""Sampler Options Model"""

from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from ibm_quantum_schemas.sampler.version_0_1.dynamical_decoupling_options import (
    DynamicalDecouplingOptionsModel,
)
from ibm_quantum_schemas.sampler.version_0_1.execution_options import (
    SamplerExecutionOptionsModel,
)
from ibm_quantum_schemas.sampler.version_0_1.simulator_options import SimulatorOptionsModel
from ibm_quantum_schemas.sampler.version_0_1.twirling_options import TwirlingOptionsModel


class OptionsModel(BaseModel):
    """Options for the Sampler."""

    model_config = ConfigDict(extra="forbid")

    default_shots: Annotated[int, Field(ge=1)] = 4096
    """The default number of shots to use if none are specified in the PUBs or in the run method.

    Each Sampler PUB can specify its own shots. If the ``run()`` method
    is given shots, then that value is used for all PUBs in the ``run()``
    call that do not specify their own.
    """

    dynamical_decoupling: DynamicalDecouplingOptionsModel = Field(
        default_factory=DynamicalDecouplingOptionsModel
    )
    """Dynamical decoupling options.

    See :class:`DynamicalDecouplingOptionsModel` for all available options.
    """

    execution: SamplerExecutionOptionsModel = Field(default_factory=SamplerExecutionOptionsModel)
    """Execution time options.

    See :class:`SamplerExecutionOptionsModel` for all available options.
    """

    twirling: TwirlingOptionsModel = Field(default_factory=TwirlingOptionsModel)
    """Pauli twirling options.

    See :class:`TwirlingOptionsModel` for all available options.
    """

    simulator: SimulatorOptionsModel | None = None
    """Simulator options.

    See :class:`SimulatorOptionsModel` for all available options.
    """

    experimental: dict = {}
    """Experimental options.

    These options are subject to change without notification, and stability is not guaranteed.
    """
