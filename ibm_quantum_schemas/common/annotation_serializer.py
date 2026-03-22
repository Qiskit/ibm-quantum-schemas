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

"""Serializer for samplomatic annotations."""

import io
import struct
from collections import namedtuple
from typing import Any, cast

from qiskit.circuit.annotation import Annotation, QPYSerializer
from samplomatic.annotations import ChangeBasis, InjectNoise, Twirl
from samplomatic.annotations.change_basis_mode import ChangeBasisLiteral
from samplomatic.annotations.decomposition_mode import DecompositionLiteral
from samplomatic.annotations.dressing_mode import DressingLiteral
from samplomatic.annotations.twirl import GroupLiteral

SAMPLOMATIC_ANNOTATION_PACK = "!H"
SAMPLOMATIC_ANNOTATION_SIZE = struct.calcsize(SAMPLOMATIC_ANNOTATION_PACK)
SAMPLOMATIC_ANNOTATION = namedtuple("SAMPLOMATIC_ANNOTATION", ["name_size"])

CHANGE_BASIS_ANNOTATION_PACK = "!QQQ"
CHANGE_BASIS_ANNOTATION_SIZE = struct.calcsize(CHANGE_BASIS_ANNOTATION_PACK)
CHANGE_BASIS_ANNOTATION = namedtuple(
    "CHANGE_BASIS_ANNOTATION", ["decomposition_size", "mode_size", "ref_size"]
)

INJECT_NOISE_ANNOTATION_PACK = "!QQ"
INJECT_NOISE_ANNOTATION_SIZE = struct.calcsize(INJECT_NOISE_ANNOTATION_PACK)
INJECT_NOISE_ANNOTATION = namedtuple("INJECT_NOISE_ANNOTATION", ["ref_size", "modifier_ref_size"])

TWIRL_ANNOTATION_PACK = "!QQQ"
TWIRL_ANNOTATION_SIZE = struct.calcsize(TWIRL_ANNOTATION_PACK)
TWIRL_ANNOTATION = namedtuple(
    "TWIRL_ANNOTATION", ["group_size", "dressing_size", "decomposition_size"]
)


class AnnotationSerializer(QPYSerializer):
    """Serializer for annotations in the 'samplomatic' namespace."""

    def dump_annotation(self, namespace: str, annotation: Any) -> bytes:
        """Dump annotation."""
        annotation_name = type(annotation).__name__.encode()
        samplomatic_annotation = (
            struct.pack(SAMPLOMATIC_ANNOTATION_PACK, len(annotation_name)) + annotation_name
        )
        if isinstance(annotation, ChangeBasis):
            decomposition = annotation.decomposition.encode()
            mode = annotation.mode.encode()
            ref = annotation.ref.encode()
            annotation_raw = struct.pack(
                CHANGE_BASIS_ANNOTATION_PACK, len(decomposition), len(mode), len(ref)
            )
            return samplomatic_annotation + annotation_raw + decomposition + mode + ref
        if isinstance(annotation, InjectNoise):
            ref = annotation.ref.encode()
            modifier_ref = annotation.modifier_ref.encode()
            annotation_raw = struct.pack(INJECT_NOISE_ANNOTATION_PACK, len(ref), len(modifier_ref))
            return samplomatic_annotation + annotation_raw + ref + modifier_ref
        if isinstance(annotation, Twirl):
            group = annotation.group.encode()
            dressing = annotation.dressing.encode()
            decomposition = annotation.decomposition.encode()
            annotation_raw = struct.pack(
                TWIRL_ANNOTATION_PACK, len(group), len(dressing), len(decomposition)
            )
            return samplomatic_annotation + annotation_raw + group + dressing + decomposition
        return NotImplemented

    def load_annotation(self, payload: bytes) -> Annotation:
        """Load annotation."""
        buff = io.BytesIO(payload)
        annotation = SAMPLOMATIC_ANNOTATION._make(
            struct.unpack(SAMPLOMATIC_ANNOTATION_PACK, buff.read(SAMPLOMATIC_ANNOTATION_SIZE))
        )
        if (name := buff.read(annotation.name_size).decode()) == "ChangeBasis":
            change_basis = CHANGE_BASIS_ANNOTATION._make(
                struct.unpack(
                    CHANGE_BASIS_ANNOTATION_PACK,
                    buff.read(CHANGE_BASIS_ANNOTATION_SIZE),
                )
            )
            decomposition = cast(
                DecompositionLiteral,
                buff.read(change_basis.decomposition_size).decode(),
            )
            mode = cast(
                ChangeBasisLiteral,
                buff.read(change_basis.mode_size).decode(),
            )
            ref = buff.read(change_basis.ref_size).decode()
            return ChangeBasis(decomposition, mode, ref)
        if name == "InjectNoise":
            inject_noise = INJECT_NOISE_ANNOTATION._make(
                struct.unpack(
                    INJECT_NOISE_ANNOTATION_PACK,
                    buff.read(INJECT_NOISE_ANNOTATION_SIZE),
                )
            )
            ref = buff.read(inject_noise.ref_size).decode()
            modifier_ref = buff.read(inject_noise.modifier_ref_size).decode()
            return InjectNoise(ref, modifier_ref)
        if name == "Twirl":
            twirl = TWIRL_ANNOTATION._make(
                struct.unpack(TWIRL_ANNOTATION_PACK, buff.read(TWIRL_ANNOTATION_SIZE))
            )
            group = cast(GroupLiteral, buff.read(twirl.group_size).decode())
            dressing = cast(DressingLiteral, buff.read(twirl.dressing_size).decode())
            decomposition = cast(DecompositionLiteral, buff.read(twirl.decomposition_size).decode())
            return Twirl(group, dressing, decomposition)
