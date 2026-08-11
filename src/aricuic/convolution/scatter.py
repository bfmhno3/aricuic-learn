"""Scatter-style convolution dataflow."""

import numpy as np


def conv2d_scatter(input_array: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """Apply valid cross-correlation by scattering each pixel contribution.

    Gather convolution asks: which input patch contributes to this output?
    Scatter convolution asks: which output cells receive this input pixel?
    This reverses dataflow and avoids materializing the im2col matrix.
    """
    input_array = np.asarray(input_array, dtype=np.float64)
    kernel = np.asarray(kernel, dtype=np.float64)

    if input_array.ndim == 2 and kernel.ndim == 2:
        kh, kw = kernel.shape
        h_out = input_array.shape[0] - kh + 1
        w_out = input_array.shape[1] - kw + 1
        output = np.zeros((h_out, w_out), dtype=np.float64)

        for h in range(input_array.shape[0]):
            out_h_start = max(0, h - kh + 1)
            out_h_stop = min(h + 1, h_out)
            for w in range(input_array.shape[1]):
                out_w_start = max(0, w - kw + 1)
                out_w_stop = min(w + 1, w_out)
                value = input_array[h, w]
                for out_h in range(out_h_start, out_h_stop):
                    kernel_h = h - out_h
                    for out_w in range(out_w_start, out_w_stop):
                        kernel_w = w - out_w
                        output[out_h, out_w] += (
                            value * kernel[kernel_h, kernel_w]
                        )
        return output

    if input_array.ndim == 3 and kernel.ndim == 4:
        cin, height, width = input_array.shape
        cout, kernel_cin, kh, kw = kernel.shape
        if cin != kernel_cin:
            raise ValueError("input channels must match kernel channels")

        h_out = height - kh + 1
        w_out = width - kw + 1
        output = np.zeros((cout, h_out, w_out), dtype=np.float64)

        for ci in range(cin):
            for h in range(height):
                out_h_start = max(0, h - kh + 1)
                out_h_stop = min(h + 1, h_out)
                for w in range(width):
                    out_w_start = max(0, w - kw + 1)
                    out_w_stop = min(w + 1, w_out)
                    value = input_array[ci, h, w]
                    for out_h in range(out_h_start, out_h_stop):
                        kernel_h = h - out_h
                        for out_w in range(out_w_start, out_w_stop):
                            kernel_w = w - out_w
                            for co in range(cout):
                                output[co, out_h, out_w] += (
                                    value * kernel[co, ci, kernel_h, kernel_w]
                                )
        return output

    raise ValueError(
        "expected 2D input with 2D kernel or 3D input with 4D kernel"
    )
