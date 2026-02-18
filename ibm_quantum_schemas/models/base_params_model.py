# This code is a Qiskit project.
#
# (C) Copyright IBM 2025.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""BaseParamsModel"""

from pydantic import BaseModel, Field


class BaseParamsModel(BaseModel):
    """Model of a runtime program's inner parameters."""

    schema_version: str = Field(pattern=r"v\d+.\d+")
    """Version of the params schema being used."""

    version: int | None = None
    """Version of the program.

    Some Programs are versioned, in which case this field is set to an integer value
    indicating which verison of the program to run.
    """
