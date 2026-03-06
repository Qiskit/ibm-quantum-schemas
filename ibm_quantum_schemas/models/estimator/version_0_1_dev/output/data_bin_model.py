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

"""Data bin models"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ibm_quantum_schemas.models.ndarray_wrapper_model import NdarrayWrapperModel


class DataBinObjectModel(BaseModel):
    """Data bin object model."""

    model_config = ConfigDict(extra="forbid")

    evs: NdarrayWrapperModel | None = None
    """Expectation values for the given observables."""

    stds: NdarrayWrapperModel | None = None
    """Standard errors computed from variation across twirling groups.
    If twirling is disabled, this equals `ensemble_standard_error`."""

    evs_noise_factors: NdarrayWrapperModel | None = None
    """Raw expectation values evaluated at each ZNE noise amplification factor."""

    stds_noise_factors: NdarrayWrapperModel | None = None
    """Standard errors computed from variation across twirling groups,
    reported separately for each ZNE noise factor."""

    ensemble_stds_noise_factors: NdarrayWrapperModel | None = None
    """Standard deviations assuming only shot noise (no twirling variance, no drift),
    reported for each ZNE noise factor. Useful for custom ZNE fitting."""

    evs_extrapolated: NdarrayWrapperModel | None = None
    """Expectation values predicted by the ZNE extrapolation model."""

    stds_extrapolated: NdarrayWrapperModel | None = None
    """Uncertainty of the extrapolated expectation values, based on the fit model."""

    ensemble_standard_error: NdarrayWrapperModel | None = None
    """Standard error assuming only shot noise, computed by treating all shots 
    as a single ensemble. Identical to `stds` when twirling is disabled."""


class DataBinModel(BaseModel):
    """Data bin model class."""

    model_config = ConfigDict(extra="forbid")

    field_names: list[str]
    """Names of fields contained the data bin."""

    field_types: list[str]
    """Types of fields contained the data bin."""

    shape: tuple[int, ...]
    """Data bin shape."""

    fields: DataBinObjectModel
    """Data bin fields."""


class DataBinWrapperModel(BaseModel):
    """Data bin wrapper model class."""

    model_config = ConfigDict(serialize_by_alias=True, extra="forbid")

    type_: Literal["DataBin"] = Field(default="DataBin", alias="__type__")
    """Redundant type information."""

    value_: DataBinModel = Field(alias="__value__")
    """The actual data."""
