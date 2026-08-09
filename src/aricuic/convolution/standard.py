"""Naive valid cross-correlation used as the baseline convolution."""

import numpy as np


def conv2d_naive(input_array: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """Apply valid cross-correlation with explicit sliding windows.

    The kernel is not flipped, so mathematically this is cross-correlation.
    Deep learning libraries commonly call this operation convolution.
    """
    input_array = np.asarray(input_array, dtype=np.float64)
    kernel = np.asarray(kernel, dtype=np.float64)

    if input_array.ndim == 2 and kernel.ndim == 2:
        kh, kw = kernel.shape
        h_out = input_array.shape[0] - kh + 1
        w_out = input_array.shape[1] - kw + 1
        output = np.zeros((h_out, w_out), dtype=np.float64)

        for h in range(h_out):
            for w in range(w_out):
                total = 0.0
                for i in range(kh):
                    for j in range(kw):
                        total += kernel[i, j] * input_array[h + i, w + j]
                output[h, w] = total
        return output

    if input_array.ndim == 3 and kernel.ndim == 4:
        cin, height, width = input_array.shape
        cout, kernel_cin, kh, kw = kernel.shape
        if cin != kernel_cin:
            raise ValueError("input channels must match kernel channels")

        h_out = height - kh + 1
        w_out = width - kw + 1
        output = np.zeros((cout, h_out, w_out), dtype=np.float64)

        for co in range(cout):
            for h in range(h_out):
                for w in range(w_out):
                    total = 0.0
                    for ci in range(cin):
                        for i in range(kh):
                            for j in range(kw):
                                total += kernel[co, ci, i, j] * input_array[ci, h + i, w + j]
                    output[co, h, w] = total
        return output

    raise ValueError(
        "expected 2D input with 2D kernel or 3D input with 4D kernel"
    )
