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

"""PEC Metadata Model."""

from __future__ import annotations

from pydantic import BaseModel


class PecMetadataModel(BaseModel):
    """Metadata about PEC."""

    num_randomizations_scaling: float | None = None
    """Scaling of the number of randomizations with circuit depth."""
