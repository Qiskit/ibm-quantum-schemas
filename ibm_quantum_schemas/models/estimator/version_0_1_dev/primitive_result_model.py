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

"""Primitive Result Model."""


from __future__ import annotations

from pydantic import BaseModel, Literal, Sequence

from ...typed_qpy_circuit_model import TypedQpyCircuitModel
from .dynamical_decoupling_options_model import DynamicalDecouplingOptionsModel
from .layer_noise_model import LayerNoiseWrapperModel
from .twirling_options_model import TwirlingOptionsModel
from .zne_options_model import ExtrapolatorType


class PrimitiveResultModel(BaseModel):
    """A model describing the Estimator program output."""

    schema_version: Literal["v0.1"] = "v0.1"
    """Schema version of the results."""

    pub_results: list[PubResultModel]
    """Result data from the estimator v2 job."""

    metadata: ResultsMetadataModel
    """Metadata for the estimator v2 job."""


class PubResultModel(BaseModel):
    """A model describing the Estimator program output for a single pub."""

    # data: TBD
    """Result data from the estimator v2 job."""

    metadata: PubResultMetadataModel
    """Metadata for the estimator v2 job."""


class ResultsMetadataModel(BaseModel):
    """Metadata for the estimator v2 job."""

    dynamical_decoupling: DynamicalDecouplingOptionsModel | None = None
    """Dynamical decoupling options.

    See :class:`DynamicalDecouplingOptionsModel` for all available options.
    """

    twirling: TwirlingOptionsModel | None = None
    """Pauli twirling options.

    See :class:`TwirlingOptionsModel` for all available options.
    """

    resilience: ResilienceMetadataModel | None = None
    """Metadata about resilience."""


class PubResultMetadataModel(BaseModel):
    """Metadata for the estimator v2 job."""

    pec: PecMetadataModel | None = None
    """Metadata about PEC."""

    layer_noise: LayerNoiseMetadataModel  | None = None
    """Metadata about layer noise."""

    
class LayerNoiseMetadataModel(BaseModel):
    
    noise_overhead: float | None = None
    total_mitigated_layers: int | None = None
    unique_mitigated_layers: set[tuple[TypedQpyCircuitModel, ...]] | None = None
    #unique_mitigated_layers_noise_overhead


class PecMetadataModel(BaseModel):
    """Metadata about PEC."""

    # num_randomizations_scaling
    # noise_gain


class ResilienceMetadataModel(BaseModel):
    """Metadata about resilience."""

    measure_mitigation: bool | None = None
    """Whether measure mitigation was applied for the job."""

    zne_mitigation: bool | None = None
    """Whether ZNE mitigation was applied for the job."""

    pec_mitigation: bool | None = None
    """Whether PEC mitigation was applied for the job."""

    zne: ZneMetadataModel | None = None
    """Metadata about ZNE, applicable if `zne_mitifation` is `True`."""

    layer_noise_model: list[LayerNoiseWrapperModel] | None = None
    """Noise learner results."""


class ZneMetadataModel(BaseModel):
    """Metadata about ZNE."""

    noise_factors: Sequence[float] | None
    """Noise factors used for noise amplification.
    """

    extrapolator: ExtrapolatorType | Sequence[ExtrapolatorType] | None = None
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

    extrapolated_noise_factors: Sequence[float] | None = None
    """Noise factors used to evaluate the fit extrapolation models at.
    
    The noise factors determine the
    points at which the ``extrapolator``\\s are evaluated, to be returned in the data
    fields called ``evs_extrapolated`` and ``stds_extrapolated``."""