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
from typing import Annotated

from pydantic import BaseModel, Field, JsonValue

from ...base_params_model import BaseParamsModel
from ...qpy_model import QpyModelV13ToV17
from .dynamical_decoupling_options_model import DynamicalDecouplingOptionsModel
from .measure_noise_learning_options_model import MeasureNoiseLearningOptionsModel
from .zne_options_model import ExtrapolatorType, ZneOptionsModel


class ParamsModel(BaseParamsModel):
    """A model describing the Estimator program inputs."""

    schema_version: str = "v0.1"

    # pub: TBD

    options: OptionsModel
    """Options for the Estimator."""


class OptionsModel(BaseModel):
    """Options for the Estimator."""

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

    seed_estimator: Annotated[int, Field(ge=0)] | None = None
    """Seed used to control sampling."""

    dynamical_decoupling: DynamicalDecouplingOptionsModel | None = None
    """Options for dynamical decoupling."""