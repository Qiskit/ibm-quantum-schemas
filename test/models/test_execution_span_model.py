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

"""Tests for samplex models."""

import datetime

from ibm_quantum_schemas.models.execution_span_model import BasicExecutionSpan


def test_roundtrip():
    """Test that round trips work correctly."""
    now = datetime.datetime.now()
    span = BasicExecutionSpan(start=now, stop=now + datetime.timedelta(seconds=5.1))

    encoded = span.model_dump_json()
    span_out = BasicExecutionSpan.model_validate_json(encoded)
    assert span == span_out
