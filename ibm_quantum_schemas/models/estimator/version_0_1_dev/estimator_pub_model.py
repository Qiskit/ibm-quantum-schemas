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

from typing import Annotated

from pydantic import BaseModel, Field

from ...noise_learner_v2.version_0_1_dev.layer_noise_model import NdarrayWrapperModel
from ...typed_qpy_circuit_model import TypedQpyCircuitModelV13to17
from .observables_array_model import ObservablesArrayModel


class EstimatorPubModel(BaseModel):
    """A model representing an Estimator Primitive Unified Bloc (PUB).
    
    A PUB encapsulates a single quantum circuit along with the observables to measure,
    parameter values, and optional precision requirements.
    """

    circuit: TypedQpyCircuitModelV13to17
    """The quantum circuit to execute, encoded in QPY format."""

    observables: ObservablesArrayModel
    """The observables to measure. Can be a single observable or a list of observables."""

    parameter_values: NdarrayWrapperModel
    """Parameter values for the circuit's parameters.
    
    A NumPy ndarray containing the parameter values to bind to the circuit's parameters.
    """

    precision: Annotated[float, Field(gt=0)] | None = None
    """Target precision for the expectation value estimates.
    
    If specified, this precision overrides the default precision set in the options.
    Must be a positive float value.
    """

