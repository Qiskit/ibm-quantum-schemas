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

"""Execution Span Models for Sampler V2."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ibm_quantum_schemas.common.datetime_wrapper import DatetimeWrapperModel


class DoubleSliceSpanModel(BaseModel):
    """Value model for DoubleSliceSpan execution span.

    Used for non-twirled sampler execution. References pub result data by
    assuming it is a sliceable portion where shots are the outermost slice
    and the rest is flattened.
    """

    start: DatetimeWrapperModel
    """The start time of the span, in UTC, wrapped with ``__type__`` and ``__value__``."""

    stop: DatetimeWrapperModel
    """The stop time of the span, in UTC, wrapped with ``__type__`` and ``__value__``."""

    data_slices: dict[int, list[int | list[int]]]
    """Map from pub indices to data slice tuples.

    Each value is a list: ``[shape_list, arg_start, arg_stop, shot_start, shot_stop]``

    - shape_list: ``list[int]`` - shape tuple including shots dimension
    - arg_start, arg_stop: ``int`` - slice bounds for flattened parameter values
    - shot_start, shot_stop: ``int`` - slice bounds for shots dimension
    """


class DoubleSliceSpanWrapperModel(BaseModel):
    """Wrapper model for DoubleSliceSpan execution span."""

    model_config = ConfigDict(populate_by_name=True)

    type_: Literal["DoubleSliceSpan"] = Field(default="DoubleSliceSpan", alias="__type__")
    """Type discriminator."""

    value_: DoubleSliceSpanModel = Field(alias="__value__")
    """The actual DoubleSliceSpan data."""


class TwirledSliceSpanV2Model(BaseModel):
    """Value model for TwirledSliceSpanV2 execution span.

    Used for twirled sampler execution. References pub result data that came
    from a twirled experiment with an axis for randomizations.
    """

    start: DatetimeWrapperModel
    """The start time of the span, in UTC, wrapped with ``__type__`` and ``__value__``."""

    stop: DatetimeWrapperModel
    """The stop time of the span, in UTC, wrapped with ``__type__`` and ``__value__``."""

    data_slices: dict[int, list[int | list[int] | bool]]
    """Map from pub indices to data slice tuples.

    Each value is a list:
    ``[shape_list, at_front, shape_start, shape_stop, shot_start, shot_stop, pub_shots]``

    - shape_list: ``list[int]`` - twirled shape tuple including twirling axis and shots
    - at_front: ``bool`` - whether randomizations axis is at front of shape
    - shape_start, shape_stop: ``int`` - slice bounds for flattened shape (excluding shots)
    - shot_start, shot_stop: ``int`` - slice bounds for shots per randomization
    - pub_shots: ``int`` - number of shots requested for the pub
    """


class TwirledSliceSpanV2WrapperModel(BaseModel):
    """Wrapper model for TwirledSliceSpanV2 execution span."""

    model_config = ConfigDict(populate_by_name=True)

    type_: Literal["TwirledSliceSpanV2"] = Field(default="TwirledSliceSpanV2", alias="__type__")
    """Type discriminator."""

    value_: TwirledSliceSpanV2Model = Field(alias="__value__")
    """The actual TwirledSliceSpanV2 data."""


class ExecutionSpansModel(BaseModel):
    """Value model for ExecutionSpans container.

    A collection of execution spans, where each span represents a time window
    of data collection.
    """

    spans: list[DoubleSliceSpanWrapperModel | TwirledSliceSpanV2WrapperModel]
    """List of execution spans, each wrapped with ``__type__`` and ``__value__``."""


class ExecutionSpansWrapperModel(BaseModel):
    """Wrapper model for ExecutionSpans container."""

    model_config = ConfigDict(populate_by_name=True)

    type_: Literal["ExecutionSpans"] = Field(default="ExecutionSpans", alias="__type__")
    """Type discriminator."""

    value_: ExecutionSpansModel = Field(alias="__value__")
    """The actual ExecutionSpans data."""
