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

"""Models"""

from __future__ import annotations

import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, Field, JsonValue, model_validator

from ....aliases import Self
from ...base_params_model import BaseParamsModel
from ...qpy_model import QpyModelV13ToV17


class ParamsModel(BaseParamsModel):
    """A model describing the Estimator program inputs."""

    schema_version: str = "v0.1"

    # pub: TBD

    options: OptionsModel
    """Options for the Estimator."""


class OptionsModel(BaseModel):
    """Options for the Estimator."""

    default_precision: float = 0.015625
    """The default precision to use for any PUB or ``run()``
    call that does not specify one.
    Each Estimator PUB can specify its own precision. If the ``run()`` method
    is given a precision, then that value is used for all PUBs in the ``run()``
    call that do not specify their own.
    """

    default_shots: int | None = None
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

    resilience_level: int = 1
    """How much resilience to build against errors.
    Higher levels generate more accurate results,
    at the expense of longer processing times.

    * 0: No mitigation.
    * 1: Minimal mitigation costs. Mitigate error associated with readout errors.
    * 2: Medium mitigation costs. Typically reduces bias in estimators but
      is not guaranteed to be zero bias.

    Refer to the
    `Configure error mitigation for Qiskit Runtime
    <https://quantum.cloud.ibm.com/docs/guides/configure-error-mitigation>`_ guide
    for more information about the error mitigation methods used at each level.
    """

    seed_estimator: int | None = None
    """Seed used to control sampling."""

    dynamical_decoupling: DynamicalDecouplingOptionsModel
    """Options for dynamical decoupling."""


class DynamicalDecouplingOptionsModel(BaseModel):
    """Options for dynamical decoupling (DD)."""

    enable: bool = False
    """Whether to enable DD as specified by the other options in this class."""

    sequence_type: Literal["XX", "XpXm", "XY4"] = "XX"
    """Which dynamical decoupling sequence to use.

    * ``"XX"``: use the sequence ``tau/2 - (+X) - tau - (+X) - tau/2``
    * ``"XpXm"``: use the sequence ``tau/2 - (+X) - tau - (-X) - tau/2``
    * ``"XY4"``: use the sequence
      ``tau/2 - (+X) - tau - (+Y) - tau (-X) - tau - (-Y) - tau/2``
    """

    extra_slack_distribution: Literal["middle", "edges"] = "middle"
    """Where to put extra timing delays due to rounding issues.

    Rounding issues arise because the discrete time step ``dt`` of the system cannot
    be divided. This option takes following values.

    * ``"middle"``: Put the extra slack to the interval at the middle of the sequence.
    * ``"edges"``: Divide the extra slack as evenly as possible into intervals at
      beginning and end of the sequence.
    """

    scheduling_method: Literal["alap", "asap"] = "alap"
    """Whether to schedule gates as soon as ("asap") or
    as late as ("alap") possible.
    """

    skip_reset_qubits: bool = False
    """Whether to insert DD on idle periods that immediately follow initialized/reset qubits.

    Since qubits in the ground state are less susceptible to decoherence, it can be beneficial
    to let them be while they are known to be in this state.
    """