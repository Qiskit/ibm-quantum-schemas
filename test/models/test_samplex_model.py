# This code is a Qiskit project.
#
# (C) Copyright IBM 2025, 2026.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Tests for samplex models."""

import pytest
from samplomatic.samplex import Samplex

from ibm_quantum_schemas.models.samplex_model import SamplexModelSSV1, SamplexModelSSV1ToSSV2


class TestSamplexModelSSV1:
    """Test the SamplexModelSSV1 model"""

    def test_roundtrip(self):
        """Test that round trips work correctly."""
        samplex = Samplex()
        SamplexModelSSV1.from_samplex(samplex, ssv=1).to_samplex()

    def test_unsupported_versions_raise(self):
        """Test that unsupported versions raise."""
        samplex = Samplex()

        with pytest.raises(ValueError):
            SamplexModelSSV1.from_samplex(samplex, ssv=2)


class TestSamplexModelSSV1ToSSV2:
    """Test the SamplexModelSSV1ToSSV2 model"""

    @pytest.mark.skip_if_samplomatic_too_old_for_ssv
    @pytest.mark.parametrize("ssv", [1, 2])
    def test_roundtrip(self, ssv):
        """Test that round trips work correctly."""
        samplex = Samplex()
        SamplexModelSSV1ToSSV2.from_samplex(samplex, ssv=ssv).to_samplex()
