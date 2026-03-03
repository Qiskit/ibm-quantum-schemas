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

"""SamplexModel"""

import re

from pydantic import BaseModel, Field, PrivateAttr, model_validator
from samplomatic.samplex import Samplex
from samplomatic.serialization import samplex_from_json, samplex_to_json
from samplomatic.ssv import SSV


class SamplexModel(BaseModel):
    """A QPY-encoded quantum circuit."""

    ssv: int = Field(ge=1)
    """The samplex serialization version."""

    samplex_json: str
    """A JSON string representing the samplex."""

    @model_validator(mode="after")
    def cross_validate_ssv_version(self):
        """Check that the reported version matches the encoded version."""
        encoded_ssv_match = re.search(r'"ssv\\*"\:\\*"(\d+)', self.samplex_json)
        if not encoded_ssv_match:
            raise ValueError("Could not locate the ssv of the encoded 'samplex_json'.")

        try:
            encoded_ssv = int(encoded_ssv_match.group(1))
        except Exception as exc:
            raise ValueError("Could not determine the SSV of the encoded 'samplex_json") from exc

        if self.ssv != encoded_ssv:
            raise ValueError(
                f"The 'ssv' is set to {self.ssv} but the encoded SSV version is {encoded_ssv}."
            )

        return self

    _samplex: Samplex = PrivateAttr()

    def to_samplex(self, use_cached: bool = False) -> Samplex:
        """Return a decoded samplex instance.

        When ``use_cached`` is false, or when no cached version exists, :attr:`~samplex_json` is
        decoded and loaded into a new instance. Users of this class are responsible for managing
        cached instances of the samplex and possible side-effects of their mutations.

        Args:
            use_cached: Whether to return the cached instance (if it exists).

        Returns:
            A samplex.
        """
        if not use_cached or not hasattr(self, "_samplex"):
            self._samplex = samplex_from_json(self.samplex_json)

        return self._samplex

    @classmethod
    def from_samplex(cls, samplex: Samplex, ssv: int | None = None):
        """Create a model instance from a samplex.

        The returned instance owns a reference to the provided samplex. This instance may be
        returned by :meth:`~to_samplex` depending on the value of ``use_cached``.
        Users of this class are responsible for managing cached instances of the samplex and
        possible side-effects of their mutations.

        Args:
            samplex: The samplex to encode into the model.

        Returns:
            A new model instance.
        """
        if ssv is None:
            ssv = SSV
        obj = cls(samplex_json=samplex_to_json(samplex, ssv=ssv), ssv=ssv)
        obj._samplex = samplex  # noqa: SLF001
        return obj


class SamplexModelSSV1(SamplexModel):
    """A samplex model constrained to use samplex serialization version (SSV) 1."""

    ssv: int = Field(ge=1, le=1)


class SamplexModelSSV1ToSSV2(SamplexModel):
    """A samplex model constrained to use samplex serialization versions (SSV) 1 or 2."""

    ssv: int = Field(ge=1, le=2)
