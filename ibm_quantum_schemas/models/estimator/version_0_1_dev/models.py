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


class ParamsModel(BaseParamsModel):
    """A model describing the Estimator program inputs, also known as "params"."""

    schema_version: Literal["v0.1"] = "v0.1"

    # To be continued