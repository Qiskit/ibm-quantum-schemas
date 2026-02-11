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

"""Models"""

from __future__ import annotations

import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, Field, JsonValue, model_validator

from ....aliases import Self
from ...base_params_model import BaseParamsModel
from ...qpy_model import QpyModelV13ToV17


class TypeTaggedModel(BaseModel):
    """Base class for type-tagged models."""
    
    @model_serializer(mode='wrap')
    def _serialize_with_type_tag(self, serializer, info):
        """Wrap serialization with __type__ and __value__."""
        value = serializer(self)
        type_name = self.__class__.__name__.replace('Model', '')
        return {
            "__type__": type_name,
            "__value__": value
        }


#class BitArrayValue(TypeTaggedModel):
#    """The value portion of a BitArray type tag."""
#    array: Union[list, str]  # Can be tagged ndarray or direct string
#    num_bits: int


class ParamsModel(BaseParamsModel):
    """A model describing the Estimator program inputs."""

    schema_version: str = "v0.1"

    

    # To be continued