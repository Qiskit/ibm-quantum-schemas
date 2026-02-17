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

"""Estimator PUB Model"""

import zlib
from io import BytesIO
from typing import Annotated

import numpy as np
import pybase64
from pydantic import Field, RootModel, model_validator

from ...noise_learner_v2.version_0_1_dev.layer_noise_model import NdarrayWrapperModel
from ...typed_qpy_circuit_model import TypedQpyCircuitModelV13to17
from .observables_array_model import ObservablesArrayModel


def _default_empty_ndarray_wrapper() -> NdarrayWrapperModel:
    """Create a default empty ndarray wrapper."""
    buffer = BytesIO()
    np.save(buffer, np.array([]))
    array_data = buffer.getvalue()
    compressed = zlib.compress(array_data)
    encoded = pybase64.b64encode(compressed).decode("utf-8")
    return NdarrayWrapperModel(type_="ndarray", value_=encoded)


class EstimatorPubModel(RootModel[tuple[
    TypedQpyCircuitModelV13to17,
    ObservablesArrayModel,
    NdarrayWrapperModel,
    Annotated[float, Field(gt=0)] | None
]]):
    """A model representing an Estimator Primitive Unified Bloc (PUB) as a tuple of length 4.
    
    A PUB encapsulates a single quantum circuit along with the observables to measure,
    parameter values, and optional precision requirements.
    
    Tuple elements:
    [0] circuit: The quantum circuit to execute, encoded in QPY format.
    [1] observables: The observables to measure. Can be a single observable or a list of observables.
    [2] parameter_values: Parameter values for the circuit's parameters (NumPy ndarray). Defaults to empty array.
    [3] precision: Target precision for the expectation value estimates (positive float or None). Defaults to None.
    """

    @model_validator(mode="before")
    @classmethod
    def add_defaults(cls, data):
        """Add default values for optional tuple elements."""
        if isinstance(data, (list, tuple)):
            data = list(data)
            # If only 2 elements provided, add defaults for parameter_values and precision
            if len(data) == 2:
                data.append(_default_empty_ndarray_wrapper().model_dump(by_alias=True))
                data.append(None)
            # If only 3 elements provided, add default for precision
            elif len(data) == 3:
                data.append(None)
            return tuple(data)
        return data

