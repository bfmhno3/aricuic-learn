"""Example 3: compare gather and scatter convolution dataflow."""

from pathlib import Path
from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from aricuic.convolution.scatter import conv2d_scatter
from aricuic.convolution.standard import conv2d_naive
from aricuic.visualization.plotting import save_figure


def _load_image() -> np.ndarray:
    image_path = Path("code/phase1/test_image.png")
    if image_path.exists():
        return np.array(Image.open(image_path).convert("L"), dtype=np.float64)
    rng = np.random.default_rng(1)
    return rng.integers(0, 256, size=(256, 256)).astype(np.float64)


def main() -> None:
    image = _load_image()
    kernel = np.ones((3, 3), dtype=np.float64) / 9.0

    gather = conv2d_naive(image, kernel)
    scatter = conv2d_scatter(image, kernel)
    max_diff = float(np.max(np.abs(gather - scatter)))

    print(f"Max difference: {max_diff:.6e}")
    if max_diff < 1e-10:
        print("PASS: Scatter output matches naive (max diff < 1e-10)")
    else:
        print("FAIL: Scatter output does not match naive")

    runs = 10
    naive_times = []
    scatter_times = []
    for _ in range(runs):
        start = perf_counter()
        conv2d_naive(image, kernel)
        naive_times.append(perf_counter() - start)
        start = perf_counter()
        conv2d_scatter(image, kernel)
        scatter_times.append(perf_counter() - start)

    print(f"Naive time: {np.mean(naive_times) * 1000:.2f}ms")
    print(f"Scatter time: {np.mean(scatter_times) * 1000:.2f}ms")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.text(0.1, 0.7, "Gather: output pixel pulls from input patch", fontsize=12)
    ax.text(0.1, 0.4, "Scatter: input pixel pushes to output locations", fontsize=12)
    ax.set_axis_off()
    fig.tight_layout()
    save_figure(fig, "example_03_dataflow.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
