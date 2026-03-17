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

"""Validation tests for ndarray_wrapper_model.py classes."""

from ibm_quantum_schemas.models.ndarray_wrapper import NdarrayWrapperModel


class TestSerializeByAlias:
    """Test that models with aliases serialize correctly."""

    def test_ndarray_wrapper_serializes_with_aliases(self):
        """Test that NdarrayWrapperModel serializes with aliases."""
        wrapper_dict = {"__type__": "ndarray", "__value__": "dummy"}
        model = NdarrayWrapperModel.model_validate(wrapper_dict)

        serialized = model.model_dump(mode="json")
        assert "__type__" in serialized
        assert "__value__" in serialized
        assert serialized["__type__"] == "ndarray"
        assert serialized["__value__"] == "dummy"
