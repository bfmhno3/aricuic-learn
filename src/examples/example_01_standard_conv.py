"""Example 1: verify naive cross-correlation against SciPy."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy.signal import correlate2d

from aricuic.convolution.standard import conv2d_naive
from aricuic.visualization.plotting import save_figure


def _load_image() -> np.ndarray:
    image_path = Path("code/phase1/test_image.png")
    if image_path.exists():
        return np.array(Image.open(image_path).convert("L"), dtype=np.float64)
    rng = np.random.default_rng(0)
    return rng.integers(0, 256, size=(256, 256)).astype(np.float64)


def main() -> None:
    image = _load_image()
    kernel = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float64)
    manual = conv2d_naive(image, kernel)
    scipy_result = correlate2d(image, kernel, mode="valid")
    max_diff = float(np.max(np.abs(manual - scipy_result)))

    print(f"Input shape: {image.shape}")
    print(f"Output shape: {manual.shape}")
    print(f"Max difference: {max_diff:.6e}")
    if max_diff < 1e-6:
        print("PASS: Manual convolution matches scipy")
    else:
        print("FAIL: Manual convolution does not match scipy")

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    axes[0].imshow(image, cmap="gray")
    axes[0].set_title("Input")
    axes[1].imshow(manual, cmap="viridis")
    axes[1].set_title("Manual")
    axes[2].imshow(scipy_result, cmap="viridis")
    axes[2].set_title("SciPy")
    for ax in axes:
        ax.axis("off")
    fig.tight_layout()
    save_figure(fig, "example_01_comparison.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
