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

"""All models needed for ResultsMetadataModel"""

from typing import Literal

from pydantic import BaseModel


class InputOptionsModel(BaseModel):
    """The input options used for the noise learning experiment."""

    max_layers_to_learn: int | None
    """The max number of unique layers to learn."""

    shots_per_randomization: int
    """The total number of shots to use per random learning circuit."""

    num_randomizations: int
    """The number of random circuits to use per learning circuit configuration."""

    layer_pair_depths: list[int]
    """The circuit depths (measured in number of pairs) to use in learning experiments."""

    twirling_strategy: Literal["active", "active-circuit", "active-accum", "all"]
    """The twirling strategy in the identified layers of two-qubit twirled gates."""


class ResultsMetadataModel(BaseModel):
    """Metadata attached to noise learner v2 results.

    Contains information about the execution context and options used during
    the noise learning experiment.
    """

    backend: str
    """The name of the backend on which the noise learning was performed."""

    input_options: InputOptionsModel
    """The input options used for the noise learning experiment."""
