"""Matplotlib helpers for the reproduction figures."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

RESULT_DIR = Path("results/figures")


def ensure_results_dir() -> None:
    """Create the figure output directory if needed."""
    RESULT_DIR.mkdir(parents=True, exist_ok=True)


def save_figure(fig: plt.Figure, name: str) -> None:
    """Save a figure under results/figures."""
    ensure_results_dir()
    fig.savefig(RESULT_DIR / name, dpi=150, bbox_inches="tight")


def _reshape_axes(axes: np.ndarray, rows: int, cols: int) -> np.ndarray:
    axes_array = np.asarray(axes, dtype=object)
    return axes_array.reshape(rows, cols)


def plot_convolution_comparison(
    image: np.ndarray, kernels: list[np.ndarray], results: list[np.ndarray], titles: list[str]
) -> None:
    """Show the source image, kernels, and resulting feature maps."""
    cols = max(1, len(results))
    fig, axes = plt.subplots(3, cols, figsize=(4 * cols, 9))
    axes = _reshape_axes(axes, 3, cols)
    image = np.asarray(image)
    for idx in range(cols):
        axes[0, idx].imshow(image, cmap="gray")
        axes[0, idx].set_title("Input")
        axes[1, idx].imshow(np.asarray(kernels[idx]), cmap="gray")
        axes[1, idx].set_title(f"Kernel: {titles[idx]}")
        axes[2, idx].imshow(np.asarray(results[idx]), cmap="viridis")
        axes[2, idx].set_title(titles[idx])
        for row in range(3):
            axes[row, idx].axis("off")
    fig.tight_layout()
    save_figure(fig, "comparison.png")
    plt.close(fig)


def plot_rotation_invariance_test(
    image: np.ndarray, angles: list[float], results: list[np.ndarray]
) -> None:
    """Plot responses over angle and show rotated inputs."""
    magnitudes = [float(np.sqrt(np.mean(np.asarray(result, dtype=np.float64) ** 2))) for result in results]
    cols = max(1, len(angles))
    fig, axes = plt.subplots(2, cols, figsize=(3 * cols, 6))
    axes = _reshape_axes(axes, 2, cols)
    for idx, angle in enumerate(angles):
        axes[0, idx].imshow(np.asarray(image), cmap="gray")
        axes[0, idx].set_title(f"{angle:.0f}°")
        axes[0, idx].axis("off")
        axes[1, idx].imshow(np.asarray(results[idx]), cmap="viridis")
        axes[1, idx].axis("off")
    fig.tight_layout()
    ensure_results_dir()
    fig.savefig(RESULT_DIR / "invariance_grid.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.plot(angles, magnitudes, marker="o")
    ax2.set_xlabel("Angle (degrees)")
    ax2.set_ylabel("Response RMS")
    ax2.set_title("Rotation response magnitude")
    ax2.grid(True, alpha=0.3)
    save_figure(fig2, "invariance_plot.png")
    plt.close(fig2)


def plot_kernel_rotations(
    kernel: np.ndarray, rotations: list[np.ndarray], angles: list[float]
) -> None:
    """Display one kernel and its rotated variants."""
    fig, axes = plt.subplots(1, len(rotations) + 1, figsize=(3 * (len(rotations) + 1), 3))
    axes = np.atleast_1d(axes)
    axes[0].imshow(np.asarray(kernel), cmap="gray")
    axes[0].set_title("0°")
    axes[0].axis("off")
    for idx, rotation in enumerate(rotations, start=1):
        axes[idx].imshow(np.asarray(rotation), cmap="gray")
        axes[idx].set_title(f"{angles[idx - 1]:.0f}°")
        axes[idx].axis("off")
    fig.tight_layout()
    save_figure(fig, "kernel_rotations.png")
    plt.close(fig)


def plot_timing_comparison(
    methods: list[str], times: list[float], speedups: list[float] | None = None
) -> None:
    """Plot method timings and optional speedup annotations."""
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(methods, times, color=["#4C78A8", "#F58518", "#54A24B", "#E45756"][: len(methods)])
    ax.set_ylabel("Seconds")
    ax.set_title("Timing comparison")
    for bar, time_value in zip(bars, times, strict=False):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            time_value,
            f"{time_value:.4f}",
            ha="center",
            va="bottom",
        )
    if speedups is not None:
        for idx, speedup in enumerate(speedups):
            ax.text(idx, times[idx], f"{speedup:.2f}x", ha="center", va="top")
    fig.tight_layout()
    save_figure(fig, "timing_comparison.png")
    plt.close(fig)


def plot_p4_orientations(orientation_maps: np.ndarray) -> None:
    """Show the four orientation channels before pooling."""
    orientation_maps = np.asarray(orientation_maps)
    fig, axes = plt.subplots(1, orientation_maps.shape[0], figsize=(4 * orientation_maps.shape[0], 4))
    axes = np.atleast_1d(axes)
    for idx, ax in enumerate(axes):
        ax.imshow(orientation_maps[idx], cmap="viridis")
        ax.set_title(f"Orientation {idx}")
        ax.axis("off")
    fig.tight_layout()
    save_figure(fig, "p4_orientations.png")
    plt.close(fig)
