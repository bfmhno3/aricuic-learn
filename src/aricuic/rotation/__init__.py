"""Rotation-equivariant and steerable convolution helpers."""

from aricuic.rotation.p4_group import p4_conv_naive, p4_conv_scatter_optimized
from aricuic.rotation.steerable import (
    arbitrary_rotation_conv,
    create_steerable_basis,
    steer_filter,
)
from aricuic.rotation.transforms import (
    get_p4_rotations,
    rotate_kernel_90,
    rotate_kernel_arbitrary,
)

__all__ = [
    "arbitrary_rotation_conv",
    "create_steerable_basis",
    "get_p4_rotations",
    "p4_conv_naive",
    "p4_conv_scatter_optimized",
    "rotate_kernel_90",
    "rotate_kernel_arbitrary",
    "steer_filter",
]
