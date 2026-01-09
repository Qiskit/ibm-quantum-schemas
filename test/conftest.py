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

"""Pytest configuration and fixtures."""

import pytest
from qiskit.qpy import QPY_VERSION
from samplomatic.ssv import SSV


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "skip_if_qiskit_too_old_for_qpy: Skip test if qpy_version parameter exceeds QPY_VERSION.",
    )

    config.addinivalue_line(
        "markers",
        "skip_if_samplomatic_too_old_for_ssv: Skip test if ssv parameter exceeds SSV.",
    )


def pytest_runtest_setup(item):
    """Setup for tests."""
    # skip a test it requires a qpy_version newer than currently installed qiskit supports
    if item.get_closest_marker("skip_if_qiskit_too_old_for_qpy") is not None:
        qpy_version = item.callspec.params.get("qpy_version")
        if qpy_version is not None and qpy_version > QPY_VERSION:
            pytest.skip(
                f"qpy_version={qpy_version} exceeds QPY_VERSION={QPY_VERSION}, a newer version of "
                "qiskit is required."
            )

    # skip a test it requires an ssv newer than currently installed samplomatic supports
    if item.get_closest_marker("skip_if_samplomatic_too_old_for_ssv") is not None:
        ssv = item.callspec.params.get("ssv")
        if ssv is not None and ssv > SSV:
            pytest.skip(
                f"ssv={ssv} exceeds SSV={QPY_VERSION}, a newer version of samplomatic is required."
            )
