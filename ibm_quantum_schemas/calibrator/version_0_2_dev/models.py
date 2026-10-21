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

    schema_version: Literal["v0.2"] = "v0.2"

    options: OptionsModel
    """Options for runtime."""


class ReadoutAngleOptions(BaseModel):
    """Options for readout angle calibration."""

    enable: bool = True
    """Whether to perform readout angle calibration."""


class OneAndTwoQubitOptions(BaseModel):
    """Options for one-and-two-qubit calibration."""

    enable: bool = False
    """Whether to perform one-and-two-qubit calibration."""


class TwoQubitOptions(BaseModel):
    """Options for two-qubit calibration."""

    enable: bool = False
    """Whether to perform two-qubit calibration."""


class TwoQubitFractionalOptions(BaseModel):
    """Options for two-qubit fractional calibration."""

    enable: bool = False
    """Whether to perform two-qubit fractional calibration."""


class TlsBiasOptions(BaseModel):
    """Options for TLS bias calibration."""

    enable: bool = False
    """Whether to perform TLS bias calibration."""


class OptionsModel(BaseModel):
    """Runtime options."""

    readout_angle: ReadoutAngleOptions = Field(default_factory=ReadoutAngleOptions)
    """Options for readout angle calibration."""

    one_and_two_qubit: OneAndTwoQubitOptions = Field(default_factory=OneAndTwoQubitOptions)
    """Options for one-and-two-qubit calibration."""

    two_qubit: TwoQubitOptions = Field(default_factory=TwoQubitOptions)
    """Options for two-qubit calibration."""

    two_qubit_fractional: TwoQubitFractionalOptions = Field(
        default_factory=TwoQubitFractionalOptions
    )
    """Options for two-qubit fractional calibration."""

    tls_bias: TlsBiasOptions = Field(default_factory=TlsBiasOptions)
    """Options for TLS bias calibration."""

    experimental: dict[str, JsonValue] = Field(default_factory=dict)
    """Experimental options.

    These options are not guaranteed to be stable and may change or be removed without notice.
    """


class CalibratorResultModel(BaseModel):
    """Result from executing a calibrator program."""

    schema_version: Literal["v0.2"] = "v0.2"
    """Schema version of the result type."""

    start: datetime.datetime
    """The start time of the calibration in UTC."""

    stop: datetime.datetime
    """The stop time of the calibration in UTC."""
