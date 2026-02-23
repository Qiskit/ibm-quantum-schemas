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

"""Measure Noise Learning Options Model"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


class MeasureNoiseLearningOptionsModel(BaseModel):
    """Options for measurement noise learning. This is only used by V2 Estimator.

    .. note::
        These options are only used when the resilience level or options specify a
        technique that requires measurement noise learning.
    """

    model_config = ConfigDict(extra="forbid")

    num_randomizations: Annotated[int, Field(ge=1)] = 32
    """The number of random circuits to draw for the measurement learning experiment."""

    shots_per_randomization: Annotated[int, Field(ge=1)] | Literal["auto"] = "auto"
    """The number of shots to use for the learning experiment per random circuit.
    
    If "auto", the value will be chosen automatically based on the input PUBs.
    """
