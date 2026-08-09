"""Naive and optimized p4 group convolutions."""

import numpy as np

from aricuic.convolution.scatter import conv2d_scatter
from aricuic.rotation.transforms import get_p4_rotations


def _pool_orientations(orientations: list[np.ndarray], pooling: str) -> np.ndarray:
    stack = np.stack(orientations, axis=0)
    if pooling == "max":
        return np.max(stack, axis=0)
    if pooling == "avg":
        return np.mean(stack, axis=0)
    raise ValueError("pooling must be 'max' or 'avg'")


def p4_orientation_maps_naive(input_array: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """Return the four orientation feature maps before pooling."""
    orientations = [conv2d_scatter(input_array, rotated) for rotated in get_p4_rotations(kernel)]
    return np.stack(orientations, axis=0)


def p4_conv_naive(
    input_array: np.ndarray, kernel: np.ndarray, pooling: str = "max"
) -> np.ndarray:
    """Apply the four rotated kernels independently, then pool orientation channels."""
    return _pool_orientations(list(p4_orientation_maps_naive(input_array, kernel)), pooling)


def p4_orientation_maps_scatter_optimized(
    input_array: np.ndarray, kernel: np.ndarray
) -> np.ndarray:
    """Compute one multiplication per input/kernel pair, then scatter to all rotations."""
    input_array = np.asarray(input_array, dtype=np.float64)
    kernel = np.asarray(kernel, dtype=np.float64)

    if input_array.ndim != 2 or kernel.ndim != 2:
        raise ValueError("optimized p4 implementation expects 2D input and 2D kernel")

    kh, kw = kernel.shape
    h_out = input_array.shape[0] - kh + 1
    w_out = input_array.shape[1] - kw + 1
    orientations = np.zeros((4, h_out, w_out), dtype=np.float64)

    for h in range(input_array.shape[0]):
        out_h_start = max(0, h - kh + 1)
        out_h_stop = min(h + 1, h_out)
        for w in range(input_array.shape[1]):
            value = input_array[h, w]
            out_w_start = max(0, w - kw + 1)
            out_w_stop = min(w + 1, w_out)
            for out_h in range(out_h_start, out_h_stop):
                offset_h = h - out_h
                for out_w in range(out_w_start, out_w_stop):
                    offset_w = w - out_w
                    orientations[0, out_h, out_w] += value * kernel[offset_h, offset_w]
                    orientations[1, out_h, out_w] += value * kernel[offset_w, kw - 1 - offset_h]
                    orientations[2, out_h, out_w] += value * kernel[kh - 1 - offset_h, kw - 1 - offset_w]
                    orientations[3, out_h, out_w] += value * kernel[kh - 1 - offset_w, offset_h]
    return orientations


def p4_conv_scatter_optimized(
    input_array: np.ndarray, kernel: np.ndarray, pooling: str = "max"
) -> np.ndarray:
    """Pool the four orientation maps from the optimized scatter pass."""
    orientations = p4_orientation_maps_scatter_optimized(input_array, kernel)
    return _pool_orientations(list(orientations), pooling)
