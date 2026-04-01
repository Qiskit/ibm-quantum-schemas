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

"""Pub Result ZNE Metadata Model."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from pydantic import BaseModel

PubResultExtrapolatorType = Literal[
    "linear",
    "exponential",
    "double_exponential",
    "polynomial_degree_1",
    "polynomial_degree_2",
    "polynomial_degree_3",
    "polynomial_degree_4",
    "polynomial_degree_5",
    "polynomial_degree_6",
    "polynomial_degree_7",
    "fallback",
]


class PubResultZneMetadataModel(BaseModel):
    """Pub Result Metadata about ZNE."""

    extrapolator: PubResultExtrapolatorType | Sequence[PubResultExtrapolatorType] | None = None
    """Extrapolator(s) used for extrapolating to zero noise.

    The available extrapolators are:

    * ``"exponential"``, which fits the data using an exponential decaying
      function defined as :math:`f(x; A, \\tau) = A e^{-x/\\tau}`, where
      :math:`A = f(0; A, \\tau)` is the value at zero noise (:math:`x=0`)
      and :math:`\\tau>0` is a positive rate.
    * ``"double_exponential"``, which uses a sum of two exponential as in Ref. 1.
    * ``"polynomial_degree_(1 <= k <= 7)"``, which uses a polynomial function defined as
      :math:`f(x; c_0, c_1, \\ldots, c_k) = \\sum_{i=0, k} c_i x^i`.
    * ``"linear"``, which is equivalent to ``"polynomial_degree_1"``.
    * ``"fallback"``, which simply returns the raw data corresponding to the lowest noise
      factor (typically ``1``) without performing any sort of extrapolation.

    The extrapolated values (``evs_extrapolated`` and ``stds_extrapolated``) are
    sorted according to the order of the provided extrapolators. If more than one
    extrapolator is specified, the ``evs`` and ``stds`` reported in the result's
    data refer to the first successful extrapolator, where an
    extrapolator success is determined heuristically.
    """
