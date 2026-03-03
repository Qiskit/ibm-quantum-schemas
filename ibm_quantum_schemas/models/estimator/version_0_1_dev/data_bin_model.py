# This code is part of Qiskit.
#
# (C) Copyright IBM 2024.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Data bin models"""

from pydantic import BaseModel, ConfigDict, Field
from typing import Literal

from ibm_quantum_schemas.models.ndarray_wrapper_model import NdarrayWrapperModel


class DataBinObjectModel(BaseModel):
    evs: NdarrayWrapperModel | None = None
    stds: NdarrayWrapperModel | None = None
    evs_noise_factors: NdarrayWrapperModel | None = None
    stds_noise_factors: NdarrayWrapperModel | None = None
    ensemble_stds_noise_factors: NdarrayWrapperModel | None = None
    evs_extrapolated: NdarrayWrapperModel | None = None
    stds_extrapolated: NdarrayWrapperModel | None = None


class DataBinModel(BaseModel):
    """Data bin model class.
    """

    field_names: list[str]
    field_types: list[str]
    shape: tuple[int, ...]
    fields: DataBinObjectModel
    

class DataBinWrapperModel(BaseModel):
    """Data bin wrapper model class.
    """
    
    model_config = ConfigDict(serialize_by_alias=True)

    type_: Literal["DataBin"] = Field(default="DataBin", alias="__type__")
    """Redundant type information."""

    value_: DataBinModel = Field(alias="__value__")
