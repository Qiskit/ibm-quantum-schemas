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

"""Sampler PUB Model"""

from typing import Annotated

from pydantic import Field, RootModel

from ibm_quantum_schemas.common.ndarray_wrapper import NdarrayWrapperModel
from ibm_quantum_schemas.common.typed_qpy_circuit import TypedQpyCircuitModelV13to17


class SamplerPubModel(
    RootModel[
        tuple[
            TypedQpyCircuitModelV13to17 | str,
            NdarrayWrapperModel,
            Annotated[int, Field(gt=0)],
        ]
    ]
):
    """A model representing a Sampler Primitive Unified Bloc (PUB) as a tuple of length 3.

    A PUB encapsulates a single quantum circuit along with parameter values and shots.

    Tuple elements:

    - [0] circuit: The quantum circuit to execute, encoded in QPY format or as a QASM string.
    - [1] parameter_values: Parameter values for the circuit's parameters (NumPy ndarray).
    - [2] shots: The number of shots to execute for this PUB.
    """
