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

from pydantic import Field, RootModel

from ibm_quantum_schemas.common.ndarray_wrapper import NdarrayWrapperModel
from ibm_quantum_schemas.common.typed_qpy_circuit import TypedQpyCircuitModelV13to17
from ibm_quantum_schemas.estimator.version_0_1.observables_array import ObservablesArrayModel


class EstimatorPubModel(
    RootModel[
        tuple[
            TypedQpyCircuitModelV13to17 | str,
            ObservablesArrayModel,
            NdarrayWrapperModel,
            Annotated[float, Field(gt=0)] | None,
        ]
    ]
):
    """A model representing an Estimator Primitive Unified Bloc (PUB) as a tuple of length 4.

    A PUB encapsulates a single quantum circuit along with the observables to measure,
    parameter values, and optional precision requirements.

    Tuple elements:

    * [0] circuit: The quantum circuit to execute, encoded in QPY format or as a QASM string.
    * [1] observables: The observables to measure. Can be a single observable or
      a list of observables.
    * [2] parameter_values: Parameter values for the circuit's parameters (NumPy ndarray).
    * [3] precision: Target precision for the expectation value estimates
      (positive float or ``None``).
    """
