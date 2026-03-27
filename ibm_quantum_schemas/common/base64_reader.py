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

"""Base64Reader"""

from collections.abc import Iterable
from io import RawIOBase

from pybase64 import b64decode


class Base64Reader(RawIOBase):
    """A readable file-like for incrementally decoding a base64-encoded string.

    Use this reader when you only need a leading chunk of a base64-encoded string.
    If you need to read the whole thing, you are likely better off using
    ``io.BytesIO(base64decode(string))`` because it avoids the Python overhead introduced by this
    class.
    """

    def __init__(self, b64_string: str, chunk_chars: int = 4096):
        """Initialize a new instance.

        Args:
            b64_string: The base-64 string to read.
            chunk_chars: How many characters to decode at a time.
        """
        if chunk_chars % 4 != 0:
            raise ValueError("chunk_chars must be a multiple of 4")

        self._iter = self._iter_b64decoded_bytes(b64_string, chunk_chars)
        self._buffer = b""

    @staticmethod
    def _iter_b64decoded_bytes(b64_string: str, chunk_chars: int = 4096) -> Iterable[bytes]:
        tail = ""

        for i in range(0, len(b64_string), chunk_chars):
            chunk = tail + b64_string[i : i + chunk_chars]

            # Only decode full 4-char blocks
            valid_len = (len(chunk) // 4) * 4
            to_decode, tail = chunk[:valid_len], chunk[valid_len:]

            if to_decode:
                yield b64decode(to_decode)

        if tail:
            yield b64decode(tail)

    def read(self, size: int = -1):
        """Read a given number of bytes from the string.

        Args:
            size: How many characters to read from the current position, where ``-1`` indicates to
                read until the end of the file.

        Returns:
            The characters.
        """
        while size < 0 or len(self._buffer) < size:
            try:
                self._buffer += next(self._iter)
            except StopIteration:
                break

        if size < 0:
            out, self._buffer = self._buffer, b""
        else:
            out, self._buffer = self._buffer[:size], self._buffer[size:]
        return out
