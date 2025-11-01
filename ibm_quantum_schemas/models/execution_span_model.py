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

"""Execution Spans"""

import datetime

from pydantic import BaseModel


class BasicExecutionSpan(BaseModel):
    """Timing information about a single sub-execution.

    .. note::

        This time span may include some amount of non-QPU classical overhead.
    """

    start: datetime.datetime
    """The start time of the execution window."""

    stop: datetime.datetime
    """The stop time of the execution window."""
