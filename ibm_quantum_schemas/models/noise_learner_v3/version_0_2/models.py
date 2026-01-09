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

"""Models"""

from __future__ import annotations

from typing import Literal, Union

from pydantic import BaseModel, Field, confloat

from ...base_params_model import BaseParamsModel
from ...qpy_model import QpyModelV13ToV16
from ...tensor_model import F64TensorModel


class ParamsModel(BaseParamsModel):
    """Schema version 1 of the inner parameters."""

    schema_version: Literal["v0.2"] = "v0.2"

    instructions: QpyModelV13ToV16
    """The instructions targeted by the noise learner.

    These are embedded to a circuit prior to encoding with QPY.
    """

    options: OptionsModel
    """Options for runtime."""


class PostSelectionOptionsModel(BaseModel):
    """Runtime options for post selection."""

    enable: bool = False
    """Whether to enable Post Selection when performing learning experiments.

    If ``False``, all the other Post Selection options are ignored.
    """

    x_pulse_type: Literal["xslow", "rx"] = "xslow"
    """The type of the X-pulse used for the post selection measurements."""

    strategy: Literal["node", "edge"] = "node"
    """The strategy used to decide if a shot should be kept or discarded."""


class OptionsModel(BaseModel):
    """Runtime options with all fields set."""

    shots_per_randomization: int = 128
    """The total number of shots to use per randomized learning circuit."""

    num_randomizations: int = 32
    """The number of random circuits to use per learning circuit configuration."""

    layer_pair_depths: list[int] = [0, 1, 2, 4, 16, 32]
    """The circuit depths (measured in number of pairs) to use in Pauli Lindblad experiments."""

    post_selection: PostSelectionOptionsModel = Field(default_factory=PostSelectionOptionsModel)
    """Options for post selecting the results of noise learning circuits."""


class PostSelectionMetadataModel(BaseModel):
    """The post selection metadata used for the results of a noise learner v3 job."""

    fraction_kept: float = Field(ge=0, le=1)
    """The fraction of shots kept."""

    success_rates: dict[int, confloat(ge=0, le=1)]  # type: ignore
    """The fraction of shots in which post selection successfully flipped each qubit."""


class TREXResultMetadataModel(BaseModel):
    """The metadata of a single TREX result of a noise learner v3 job."""

    learning_protocol: Literal["trex"] = "trex"
    """The learning protocol used to obtain this result."""

    post_selection: PostSelectionMetadataModel
    """The post selection metadata."""


class LinbdbladResultMetadataModel(BaseModel):
    """The metadata of a single Lindblad result of a noise learner v3 job."""

    learning_protocol: Literal["lindblad"] = "lindblad"
    """The learning protocol used to obtain this result."""

    post_selection: dict[int, PostSelectionMetadataModel]
    """The post selection metadata obtained for each layer pair depth."""


class NoiseLearnerV3ResultModel(BaseModel):
    """Results for a single noise learner V3 item."""

    generators_sparse: list[list[tuple[str, list[int]]]]
    """A representation of the generators in sparse format."""

    num_qubits: int
    """The number of qubits that the generators act on."""

    rates: F64TensorModel
    """The rates of the individual generators."""

    rates_std: F64TensorModel
    """The standard deviation associated to the rates of the generators."""

    metadata: Union[TREXResultMetadataModel, LinbdbladResultMetadataModel] = Field(
        discriminator="learning_protocol"
    )
    """Execution metadata pertaining to a single result."""


class NoiseLearnerV3ResultsModel(BaseModel):
    """Result from executing a noise learner v3 job."""

    schema_version: Literal["v0.2"] = "v0.2"
    """Schema version of the result type."""

    data: list[NoiseLearnerV3ResultModel]
    """Resulting data for each item."""
