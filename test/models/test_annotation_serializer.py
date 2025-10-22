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

"""Tests for annotation serializers."""

from samplomatic import ChangeBasis, InjectNoise, Twirl

from ibm_quantum_schemas.models.annotation_serializer import AnnotationSerializer


class TestChangeBasis:
    """Tests for ``ChangeBasis``."""

    def test_roundtrip(self):
        """Test that round trips work correctly."""
        annotation = ChangeBasis()
        namespace = "samplomatic.change_basis"

        serializer = AnnotationSerializer()
        payload = serializer.dump_annotation(namespace, annotation)
        annotation_out = serializer.load_annotation(payload)

        assert annotation == annotation_out


class TestInjectNoise:
    """Tests for ``InjectNoise``."""

    def test_roundtrip(self):
        """Test that round trips work correctly."""
        annotation = InjectNoise("ref")
        namespace = "samplomatic.inject_noise"

        serializer = AnnotationSerializer()
        payload = serializer.dump_annotation(namespace, annotation)
        annotation_out = serializer.load_annotation(payload)

        assert annotation == annotation_out


class TestTwirl:
    """Tests for ``Twirl``."""

    def test_roundtrip(self):
        """Test that round trips work correctly."""
        annotation = Twirl()
        namespace = "samplomatic.twirl"

        serializer = AnnotationSerializer()
        payload = serializer.dump_annotation(namespace, annotation)
        annotation_out = serializer.load_annotation(payload)

        assert annotation == annotation_out
