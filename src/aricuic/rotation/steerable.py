"""Steerable filter helpers for arbitrary-angle responses."""

import math

import numpy as np
from scipy import ndimage

from aricuic.convolution.standard import conv2d_naive
from aricuic.rotation.transforms import rotate_kernel_90


def create_steerable_basis(ksize: int) -> tuple[np.ndarray, np.ndarray]:
    """Create simple horizontal and vertical Sobel-style basis filters."""
    if ksize != 3:
        raise ValueError("this educational implementation expects a 3x3 basis")
    fx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float64)
    fy = rotate_kernel_90(fx)
    return fx, fy


def steer_filter(fx: np.ndarray, fy: np.ndarray, angle: float) -> np.ndarray:
    """Interpolate basis filters using the paper's steering equation."""
    theta = math.radians(angle)
    return np.sin(theta) * np.asarray(fx, dtype=np.float64) + np.cos(
        theta
    ) * np.asarray(fy, dtype=np.float64)


def arbitrary_rotation_conv(
    input_array: np.ndarray,
    fx: np.ndarray,
    fy: np.ndarray,
    angles: list[float],
) -> dict[float, np.ndarray]:
    """Apply steerable filters for the requested angles.

    Angles in the first quadrant are steered directly. Other quadrants are
    reduced to an equivalent acute angle and then mapped back by symmetry.
    """
    input_array = np.asarray(input_array, dtype=np.float64)
    results: dict[float, np.ndarray] = {}
    for angle in angles:
        normalized = angle % 360.0
        if normalized <= 90.0:
            kernel = steer_filter(fx, fy, normalized)
        elif normalized <= 180.0:
            kernel = rotate_kernel_90(steer_filter(fx, fy, normalized - 90.0))
        elif normalized <= 270.0:
            kernel = np.rot90(steer_filter(fx, fy, normalized - 180.0), k=2)
        else:
            kernel = np.rot90(steer_filter(fx, fy, normalized - 270.0), k=3)
        results[angle] = conv2d_naive(input_array, kernel)
    return results


def rotated_kernel_with_interpolation(
    kernel: np.ndarray, angle: float
) -> np.ndarray:
    """Rotate a kernel by interpolation for visual comparison."""
    return ndimage.rotate(
        np.asarray(kernel, dtype=np.float64),
        angle=angle,
        reshape=False,
        order=1,
        mode="constant",
        cval=0.0,
    )
