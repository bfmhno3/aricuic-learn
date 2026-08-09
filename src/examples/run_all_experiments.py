"""Run all reproduction examples and summarize their outcomes."""

import runpy
import time
from pathlib import Path

from tqdm import tqdm

EXAMPLES = [
    "src/examples/example_01_standard_conv.py",
    "src/examples/example_02_im2col_demo.py",
    "src/examples/example_03_scatter_conv.py",
    "src/examples/example_04_kernel_rotation.py",
    "src/examples/example_05_p4_group.py",
    "src/examples/example_06_rotation_invariance.py",
    "src/examples/example_07_steerable_filters.py",
]


def main() -> None:
    Path("results/figures").mkdir(parents=True, exist_ok=True)
    summaries: list[tuple[str, str, float, str]] = []
    for script in tqdm(EXAMPLES, desc="Running examples"):
        start = time.perf_counter()
        status = "PASS"
        error = ""
        try:
            runpy.run_path(script, run_name="__main__")
        except Exception as exc:  # noqa: BLE001 - keep the runner going for the report.
            status = "FAIL"
            error = f"{type(exc).__name__}: {exc}"
        elapsed = time.perf_counter() - start
        summaries.append((script, status, elapsed, error))

    report = Path("results/experiment_summary.txt")
    with report.open("w", encoding="utf-8") as handle:
        for script, status, elapsed, error in summaries:
            handle.write(f"{script}\t{status}\t{elapsed:.4f}s\t{error}\n")
    print(f"Wrote {report}")


if __name__ == "__main__":
    main()
