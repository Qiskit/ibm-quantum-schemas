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

"""Primitive Result Model."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ibm_quantum_schemas.estimator.version_0_1.dynamical_decoupling_metadata import (
    DynamicalDecouplingMetadataModel,
)
from ibm_quantum_schemas.estimator.version_0_1.primitive_result_resilience_metadata import (
    PrimitiveResultResilienceMetadataModel,
)
from ibm_quantum_schemas.estimator.version_0_1.pub_result import PubResultWrapperModel
from ibm_quantum_schemas.estimator.version_0_1.twirling_metadata import TwirlingMetadataModel


class PrimitiveResultMetadataModel(BaseModel):
    """Metadata for the estimator v2 job."""

    dynamical_decoupling: DynamicalDecouplingMetadataModel | None = None
    """Dynamical decoupling metadata."""

    twirling: TwirlingMetadataModel | None = None
    """Pauli twirling metadata."""

    resilience: PrimitiveResultResilienceMetadataModel | None = None
    """Metadata about resilience."""

    version: Literal[2] = 2
    """Version number. Must be 2."""


class PrimitiveResultModel(BaseModel):
    """A model describing the Estimator program output."""

    pub_results: list[PubResultWrapperModel]
    """Result data from the estimator v2 job."""

    metadata: PrimitiveResultMetadataModel
    """Metadata for the estimator v2 job."""


class PrimitiveResultWrapperModel(BaseModel):
    """Primitive result wrapper model class."""

    model_config = ConfigDict(serialize_by_alias=True)

    type_: Literal["PrimitiveResult"] = Field(default="PrimitiveResult", alias="__type__")
    """Redundant type information."""

    value_: PrimitiveResultModel = Field(alias="__value__")
    """The actual data."""
