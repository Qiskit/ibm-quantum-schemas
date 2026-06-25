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

"""
=================================================
Common models (:mod:`ibm_quantum_schemas.common`)
=================================================

.. currentmodule:: ibm_quantum_schemas.common

Models that provide common functionality.

Classes
=======

.. autosummary::
   :toctree: ../stubs/
   :nosignatures:

   QpyDataModel
   QpyDataV13ToV17Model
   QpyModel
   QpyModelV13ToV16
   QpyModelV13ToV17
   CompressedQpyDataModel
   CompressedQpyDataV13ToV17Model
   BaseParamsModel
   PauliLindbladMapModel
   SamplexModel
   SamplexModelSSV1
   SamplexModelSSV1ToSSV2
   TensorModel
   F64TensorModel
   CompressedTensorModel
   BoolCompressedTensorModel
   C128CompressedTensorModel
   F64CompressedTensorModel
   U8CompressedTensorModel
"""

from ibm_quantum_schemas.common.base_params import BaseParamsModel
from ibm_quantum_schemas.common.pauli_lindblad_map import PauliLindbladMapModel
from ibm_quantum_schemas.common.qpy import (
    CompressedQpyDataModel,
    CompressedQpyDataV13ToV17Model,
    QpyDataModel,
    QpyDataV13ToV17Model,
    QpyModel,
    QpyModelV13ToV16,
    QpyModelV13ToV17,
)
from ibm_quantum_schemas.common.samplex import (
    SamplexModel,
    SamplexModelSSV1,
    SamplexModelSSV1ToSSV2,
    SamplexModelSSV1ToSSV3,
    SamplexModelSSV1ToSSV4,
)
from ibm_quantum_schemas.common.tensor import (
    BoolCompressedTensorModel,
    C128CompressedTensorModel,
    CompressedTensorModel,
    F64CompressedTensorModel,
    F64TensorModel,
    TensorModel,
    U8CompressedTensorModel,
)
