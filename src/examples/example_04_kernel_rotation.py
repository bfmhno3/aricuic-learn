"""Example 4: rotate a Sobel kernel and compare responses."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from aricuic.convolution.standard import conv2d_naive
from aricuic.rotation.transforms import get_p4_rotations
from aricuic.visualization.plotting import (
    ensure_results_dir,
    plot_kernel_rotations,
)


def _load_image() -> np.ndarray:
    image_path = Path("code/phase1/test_image.png")
    if image_path.exists():
        return np.array(Image.open(image_path).convert("L"), dtype=np.float64)
    grid = np.indices((256, 256)).sum(axis=0) % 2
    return (grid * 255).astype(np.float64)


def main() -> None:
    image = _load_image()
    kernel = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float64)
    rotations = get_p4_rotations(kernel)
    responses = [conv2d_naive(image, rotated) for rotated in rotations]

    for angle, response in zip([0, 90, 180, 270], responses, strict=False):
        print(f"Angle {angle}° response mean: {np.mean(response):.4f}")

    plot_kernel_rotations(kernel, rotations[1:], [90, 180, 270])

    ensure_results_dir()
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    axes[0, 0].imshow(image, cmap="gray")
    axes[0, 0].set_title("Input")
    axes[0, 1].imshow(rotations[0], cmap="gray")
    axes[0, 1].set_title("0° kernel")
    axes[0, 2].imshow(rotations[1], cmap="gray")
    axes[0, 2].set_title("90° kernel")
    axes[1, 0].imshow(responses[0], cmap="viridis")
    axes[1, 0].set_title("0° response")
    axes[1, 1].imshow(responses[1], cmap="viridis")
    axes[1, 1].set_title("90° response")
    axes[1, 2].imshow(responses[2], cmap="viridis")
    axes[1, 2].set_title("180° response")
    for ax in axes.flat:
        ax.axis("off")
    fig.tight_layout()
    fig.savefig("results/figures/example_04_kernel_rotation.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
