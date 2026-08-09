"""Kernel rotation helpers for p4 and steerable examples."""

import numpy as np
from scipy import ndimage


def rotate_kernel_90(kernel: np.ndarray) -> np.ndarray:
    """Rotate a kernel 90 degrees counterclockwise."""
    return np.rot90(np.asarray(kernel, dtype=np.float64), k=1)


def rotate_kernel_arbitrary(kernel: np.ndarray, angle: float) -> np.ndarray:
    """Rotate a kernel by an arbitrary angle using interpolation."""
    return ndimage.rotate(
        np.asarray(kernel, dtype=np.float64),
        angle=angle,
        reshape=False,
        order=1,
        mode="constant",
        cval=0.0,
    )


def get_p4_rotations(kernel: np.ndarray) -> list[np.ndarray]:
    """Return the four 90-degree rotations used by the p4 group."""
    kernel = np.asarray(kernel, dtype=np.float64)
    return [np.rot90(kernel, k=k) for k in range(4)]
