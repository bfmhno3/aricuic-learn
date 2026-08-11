"""Example 6: show approximate rotation invariance after p4 pooling."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy import ndimage

from aricuic.rotation.p4_group import p4_conv_scatter_optimized
from aricuic.visualization.plotting import (
    ensure_results_dir,
    plot_rotation_invariance_test,
)


def _load_image() -> np.ndarray:
    image_path = Path("code/phase1/test_image.png")
    if image_path.exists():
        return np.array(Image.open(image_path).convert("L"), dtype=np.float64)
    grid = np.zeros((256, 256), dtype=np.float64)
    grid[96:160, 96:160] = 255.0
    return grid


def main() -> None:
    image = _load_image()
    angles = [0, 30, 45, 60, 90, 135, 180, 270]
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

    results = []
    magnitudes = []
    for angle in angles:
        rotated = ndimage.rotate(
            image,
            angle=angle,
            reshape=False,
            order=1,
            mode="constant",
            cval=0.0,
        )
        response = p4_conv_scatter_optimized(rotated, kernel, pooling="max")
        results.append(response)
        magnitudes.append(float(np.sqrt(np.mean(response**2))))

    magnitudes = np.asarray(magnitudes)
    cv = float(magnitudes.std() / magnitudes.mean())
    print(f"Rotation invariance coefficient of variation: {cv * 100:.2f}%")
    print(f"Rotation invariance CV: {cv * 100:.2f}%")

    plot_rotation_invariance_test(image, angles, results)

    ensure_results_dir()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(angles, magnitudes, marker="o")
    ax.set_xlabel("Angle")
    ax.set_ylabel("Response magnitude")
    ax.set_title("P4 pooled response stability")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(
        "results/figures/example_06_invariance_plot.png",
        dpi=150,
        bbox_inches="tight",
    )
    plt.close(fig)


if __name__ == "__main__":
    main()
