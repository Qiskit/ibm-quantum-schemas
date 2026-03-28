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

"""Params Model"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibm_quantum_schemas.estimator.version_0_1.estimator_pub import EstimatorPubModel
from ibm_quantum_schemas.estimator.version_0_1.options import OptionsModel


class ParamsModel(BaseModel):
    """A model describing the Estimator program inputs."""

    model_config = ConfigDict(extra="forbid")

    pubs: list[EstimatorPubModel]
    """List of Estimator Primitive Unified Blocs (PUBs).

    Each PUB contains a circuit, observables to measure, parameter values, and optional precision.
    """

    support_qiskit: bool = True
    """Whether to support Qiskit-specific features."""

    version: Literal[2] = 2
    """Version number. Must be 2."""

    options: OptionsModel = Field(default_factory=OptionsModel)
    """Options for the Estimator."""

    resilience_level: Annotated[int, Field(ge=0, le=2)] = 1
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
