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

"""Test Base64Reader"""

import pybase64
import pytest

from ibm_quantum_schemas.common.base64_reader import Base64Reader


def test_full_read_matches_direct_decode():
    """Reading the full stream matches direct base64 decoding."""
    data = b"The quick brown fox jumps over the lazy dog"
    b64 = pybase64.b64encode(data).decode()

    reader = Base64Reader(b64)
    result = reader.read()

    assert result == data


def test_partial_read_prefix():
    """Partial reads return the correct decoded prefix."""
    data = b"abcdefghijklmnopqrstuvwxyz"
    b64 = pybase64.b64encode(data).decode()

    reader = Base64Reader(b64)
    head = reader.read(10)

    assert head == data[:10]


def test_multiple_small_reads():
    """Multiple successive reads reconstruct the full decoded payload."""
    data = b"0123456789" * 10
    b64 = pybase64.b64encode(data).decode()

    reader = Base64Reader(b64)

    chunks = []
    for _ in range(10):
        chunks.append(reader.read(10))

    assert b"".join(chunks) == data


def test_read_past_eof():
    """Reads past EOF return empty bytes without error."""
    data = b"hello"
    b64 = pybase64.b64encode(data).decode()

    reader = Base64Reader(b64)

    assert reader.read(5) == data
    assert reader.read(5) == b""
    assert reader.read() == b""


def test_chunk_boundary_behavior():
    """Decoding remains correct across base64 chunk boundaries."""
    data = b"a" * 1000
    b64 = pybase64.b64encode(data).decode()

    reader = Base64Reader(b64, chunk_chars=8)

    out = bytearray()
    while True:
        chunk = reader.read(7)
        if not chunk:
            break
        out.extend(chunk)

    assert bytes(out) == data


def test_empty_input():
    """Empty base64 input produces empty output."""
    reader = Base64Reader("")
    assert reader.read() == b""
    assert reader.read(10) == b""


def test_binary_data():
    """Arbitrary binary data round-trips through the reader."""
    data = bytes(range(256))
    b64 = pybase64.b64encode(data).decode()

    reader = Base64Reader(b64)
    result = reader.read()

    assert result == data


def test_invalid_chunk_size():
    """Non–4-multiple chunk sizes are rejected."""
    with pytest.raises(ValueError):
        Base64Reader("AAAA", chunk_chars=5)
