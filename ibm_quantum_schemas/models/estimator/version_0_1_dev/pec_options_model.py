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

"""PEC Options Model"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Field, field_validator


class PecOptionsModel(BaseModel):
    """Probabalistic error cancellation mitigation options. This is only used by V2 Estimator."""

    max_overhead: Annotated[float, Field(gt=0)] | None = 100.0
    """The maximum circuit sampling overhead allowed, or ``None`` for no maximum."""

    noise_gain: Annotated[float, Field(ge=0)] | Literal["auto"] = "auto"
    """The amount by which to scale the noise, where:

        * A value of 0 corresponds to removing the full learned noise.
        * A value of 1 corresponds to no removal of the learned noise.
        * A value between 0 and 1 corresponds to partially removing the learned noise.
        * A value greater than one corresponds to amplifying the learned noise.

    If "auto", the value in the range ``[0, 1]`` will be chosen automatically
    for each input PUB based on the learned noise strength, ``max_overhead``,
    and the depth of the PUB.
    """

    @field_validator("noise_gain")
    @classmethod
    def _validate_noise_gain(cls, value: float | Literal["auto"]) -> float | Literal["auto"]:
        """Validate noise_gain."""
        if isinstance(value, (int, float)) and value < 0:
            raise ValueError("noise_gain must be >= 0")
        return value

