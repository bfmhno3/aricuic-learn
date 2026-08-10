"""Example 2: show how im2col duplicates input patches."""

import matplotlib.pyplot as plt
import numpy as np

from aricuic.convolution.im2col import duplication_stats, im2col
from aricuic.visualization.plotting import save_figure


def main() -> None:
    image = np.arange(1, 17, dtype=np.float64).reshape(4, 4)
    columns = im2col(image, 3, 3)
    input_elements, column_elements, duplication_factor = duplication_stats(
        image, 3, 3
    )

    print("Input matrix (4x4):")
    print(image)
    print()
    print(f"im2col output ({columns.shape[0]}x{columns.shape[1]}):")
    print(columns)
    print()
    print(f"Input elements: {input_elements}")
    print(f"Column matrix elements: {column_elements}")
    print(f"Duplication factor: {duplication_factor:.1f}")
    print("Expected (Kh*Kw): 9")

    positions = np.argwhere(columns == 6)
    print("Example: element 6 appears in these positions:")
    for row, col in positions:
        print(f"  col_matrix[{row}][{col}]")

    fig, (original_ax, im2col_ax) = plt.subplots(1, 2, figsize=(8, 4))
    original_ax.imshow(image, cmap="viridis")
    original_ax.set_title("Original image")
    original_ax.set_xlabel("Column")
    original_ax.set_ylabel("Row")

    im2col_ax.imshow(columns, cmap="viridis", aspect="auto")
    im2col_ax.set_title("im2col output")
    im2col_ax.set_xlabel("Flattened patch index")
    im2col_ax.set_ylabel("Patch row")
    fig.tight_layout()
    save_figure(fig, "example_02_im2col.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
