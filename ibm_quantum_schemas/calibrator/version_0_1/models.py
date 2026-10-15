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

"""Models for calibrator."""

from __future__ import annotations

import datetime
from typing import Literal

from pydantic import BaseModel, Field, JsonValue

from ibm_quantum_schemas.common import (
    BaseParamsModel,
)


class ParamsModel(BaseParamsModel):
    """A model describing the Calibrator program inputs."""

    schema_version: Literal["v0.1"] = "v0.1"

    options: OptionsModel
    """Options for runtime."""


class OptionsModel(BaseModel):
    """Runtime options."""

    experimental: dict[str, JsonValue] = Field(default_factory=dict)
    """Experimental options.

    These options are not guaranteed to be stable and may change or be removed without notice.
    """


class CalibratorResultModel(BaseModel):
    """Result from executing a calibrator program."""

    schema_version: Literal["v0.1"] = "v0.1"
    """Schema version of the result type."""

    start: datetime.datetime
    """The start time of the calibration in UTC."""

    stop: datetime.datetime
    """The stop time of the calibration in UTC."""
