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

from pydantic import BaseModel, PrivateAttr, field_validator
from samplomatic._version import version as _samplomatic_version
from samplomatic.samplex import Samplex
from samplomatic.serialization import samplex_from_json, samplex_to_json


class SamplexModel(BaseModel):
    """A QPY-encoded quantum circuit."""

    samplex_json: str
    """A JSON string representing the samplex."""

    samplomatic_version: str
    """The samplomatic version that generated the JSON."""

    @field_validator("samplomatic_version")
    @classmethod
    def strict_version_equality(cls, value):
        """Validate model version matches samplomatic version of local environment."""
        if value != _samplomatic_version:
            raise ValueError(
                "The samplomatic version that created the encoded samplex must be exactly equal to "
                f"{_samplomatic_version}, but {value} found instead."
            )
        return value

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
    def from_samplex(cls, samplex: Samplex):
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
        obj = cls(samplex_json=samplex_to_json(samplex), samplomatic_version=_samplomatic_version)
        obj._samplex = samplex  # noqa: SLF001
        return obj
