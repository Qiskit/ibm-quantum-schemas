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

from pydantic import BaseModel, Field, Literal

from .dynamical_decoupling_options_model import DynamicalDecouplingOptionsModel


class PrimitiveResultModel(BaseModel):
    """A model describing the Estimator program output."""

    schema_version: Literal["v0.1"] = "v0.1"
    """Schema version of the results."""

    pub_results: list[PubResultModel]
    """Result data from the estimator v2 job."""

    metadata: ResultsMetadataModel
    """Metadata for the estimator v2 job."""


class PubResultModel(BaseModel):
    """A model describing the Estimator program output for a single pub."""

    # data: TBD
    """Result data from the estimator v2 job."""

    metadata: PubResultMetadataModel
    """Metadata for the estimator v2 job."""


class ResultsMetadataModel(BaseModel):
    """Metadata for the estimator v2 job."""

    dynamical_decoupling: DynamicalDecouplingOptionsModel = Field(
        default_factory=DynamicalDecouplingOptionsModel
    )
    """Dynamical decoupling options.

    See :class:`DynamicalDecouplingOptionsModel` for all available options.
    """



class PubResultMetadataModel(BaseModel):
    """Metadata for the estimator v2 job."""

    # TBD