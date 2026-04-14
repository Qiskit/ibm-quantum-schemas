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

"""Primitive Result Model for Sampler V2."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ibm_quantum_schemas.sampler.version_0_1.execution_span import (
    ExecutionSpansWrapperModel,
)
from ibm_quantum_schemas.sampler.version_0_1.pub_result import SamplerPubResultWrapperModel


class ExecutionMetadataModel(BaseModel):
    """Execution metadata for the sampler v2 job."""

    execution_spans: ExecutionSpansWrapperModel
    """Execution span information wrapped in ExecutionSpans container.

    Contains a list of execution spans, where each span can be either:

    - DoubleSliceSpan: for non-twirled execution
    - TwirledSliceSpanV2: for twirled execution with pub_shots tracking
    """


class PrimitiveResultMetadataModel(BaseModel):
    """Metadata for the sampler v2 job."""

    execution: ExecutionMetadataModel
    """Execution metadata including spans."""

    version: Literal[2] = 2
    """Version number. Must be 2."""


class PrimitiveResultModel(BaseModel):
    """A model describing the Sampler V2 program output."""

    pub_results: list[SamplerPubResultWrapperModel]
    """Result data from the sampler v2 job."""

    metadata: PrimitiveResultMetadataModel
    """Metadata for the sampler v2 job."""


class PrimitiveResultWrapperModel(BaseModel):
    """Primitive result wrapper model class."""

    model_config = ConfigDict(serialize_by_alias=True)

    type_: Literal["PrimitiveResult"] = Field(default="PrimitiveResult", alias="__type__")
    """Redundant type information."""

    value_: PrimitiveResultModel = Field(alias="__value__")
    """The actual data."""
