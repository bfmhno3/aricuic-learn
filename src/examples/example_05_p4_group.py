"""Example 5: compare naive and optimized p4 group convolution."""

from pathlib import Path
from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from aricuic.rotation.p4_group import (
    p4_conv_naive,
    p4_conv_scatter_optimized,
    p4_orientation_maps_naive,
    p4_orientation_maps_scatter_optimized,
)
from aricuic.visualization.plotting import (
    plot_p4_orientations,
    plot_timing_comparison,
)


def _load_image() -> np.ndarray:
    image_path = Path("code/phase1/test_image.png")
    if image_path.exists():
        image = np.array(Image.open(image_path).convert("L"), dtype=np.float64)
        if image.shape[0] < 512 or image.shape[1] < 512:
            return np.tile(image, (2, 2))[:512, :512]
        return image[:512, :512]
    rng = np.random.default_rng(2)
    return rng.integers(0, 256, size=(512, 512)).astype(np.float64)


def main() -> None:
    image = _load_image()
    kernel = np.array(
        [
            [1, 4, 6, 4, 1],
            [4, 16, 24, 16, 4],
            [6, 24, 36, 24, 6],
            [4, 16, 24, 16, 4],
            [1, 4, 6, 4, 1],
        ],
        dtype=np.float64,
    )
    kernel /= kernel.sum()

    naive = p4_conv_naive(image, kernel, pooling="max")
    optimized = p4_conv_scatter_optimized(image, kernel, pooling="max")
    max_diff = float(np.max(np.abs(naive - optimized)))

    print(f"Max difference: {max_diff:.6e}")
    if max_diff < 1e-10:
        print("PASS: Optimized p4 matches naive p4 (max diff < 1e-10)")
    else:
        print("FAIL: Optimized p4 does not match naive p4")

    runs = 5
    naive_times = []
    optimized_times = []
    for _ in range(runs):
        start = perf_counter()
        p4_conv_naive(image, kernel, pooling="max")
        naive_times.append(perf_counter() - start)
        start = perf_counter()
        p4_conv_scatter_optimized(image, kernel, pooling="max")
        optimized_times.append(perf_counter() - start)

    naive_mean = float(np.mean(naive_times))
    optimized_mean = float(np.mean(optimized_times))
    speedup = naive_mean / optimized_mean if optimized_mean else float("inf")
    print(
        f"Naive: {naive_mean:.2f}s, Optimized: {optimized_mean:.2f}s, Speedup: {speedup:.2f}x"
    )

    plot_timing_comparison(
        ["Naive", "Optimized"], [naive_mean, optimized_mean], [speedup]
    )
    plot_p4_orientations(
        p4_orientation_maps_naive(image, kernel), "p4_orientations_naive.png"
    )
    plot_p4_orientations(
        p4_orientation_maps_scatter_optimized(image, kernel),
        "p4_orientations_optimized.png",
    )

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.imshow(naive, cmap="viridis")
    ax.set_title("P4 pooled response")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(
        "results/figures/example_05_p4_comparison.png",
        dpi=150,
        bbox_inches="tight",
    )
    plt.close(fig)


if __name__ == "__main__":
    main()
