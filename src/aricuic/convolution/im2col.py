"""im2col transformation and convolution-by-matrix-multiply."""

import numpy as np


def im2col(input_array: np.ndarray, kh: int, kw: int) -> np.ndarray:
    """Flatten each valid receptive field into one column.

    Each input pixel may be copied up to Kh * Kw times, which is the memory
    duplication cost that scatter-style convolution avoids.
    """
    input_array = np.asarray(input_array, dtype=np.float64)
    if input_array.ndim == 2:
        input_array = input_array[np.newaxis, :, :]
    if input_array.ndim != 3:
        raise ValueError("input must have shape (H, W) or (C, H, W)")

    channels, height, width = input_array.shape
    h_out = height - kh + 1
    w_out = width - kw + 1
    columns = np.zeros((channels * kh * kw, h_out * w_out), dtype=np.float64)

    for h in range(h_out):
        for w in range(w_out):
            col_idx = h * w_out + w
            for c in range(channels):
                for i in range(kh):
                    for j in range(kw):
                        row_idx = c * kh * kw + i * kw + j
                        columns[row_idx, col_idx] = input_array[c, h + i, w + j]
    return columns


def conv2d_im2col(input_array: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """Apply valid cross-correlation using im2col plus matrix multiply."""
    input_array = np.asarray(input_array, dtype=np.float64)
    kernel = np.asarray(kernel, dtype=np.float64)

    if input_array.ndim == 2 and kernel.ndim == 2:
        kh, kw = kernel.shape
        columns = im2col(input_array, kh, kw)
        flat_kernel = kernel.reshape(1, kh * kw)
        result = flat_kernel @ columns
        h_out = input_array.shape[0] - kh + 1
        w_out = input_array.shape[1] - kw + 1
        return result.reshape(h_out, w_out)

    if input_array.ndim == 3 and kernel.ndim == 4:
        cout, cin, kh, kw = kernel.shape
        if input_array.shape[0] != cin:
            raise ValueError("input channels must match kernel channels")
        columns = im2col(input_array, kh, kw)
        flat_kernel = kernel.reshape(cout, cin * kh * kw)
        result = flat_kernel @ columns
        h_out = input_array.shape[1] - kh + 1
        w_out = input_array.shape[2] - kw + 1
        return result.reshape(cout, h_out, w_out)

    raise ValueError(
        "expected 2D input with 2D kernel or 3D input with 4D kernel"
    )


def duplication_stats(input_array: np.ndarray, kh: int, kw: int) -> tuple[int, int, float]:
    """Return input size, column matrix size, and duplication factor."""
    input_array = np.asarray(input_array)
    input_elements = input_array.size
    column_elements = im2col(input_array, kh, kw).size
    return input_elements, column_elements, column_elements / input_elements
