import sys
import warnings
from pathlib import Path

import matplotlib
import pytest

import hepi.data
from hepi.fast import main

matplotlib.use("Agg", force=True)
from matplotlib import pyplot as plt


GRID_FILES = sorted(
    filename for filename in hepi.data.list_files() if filename.endswith(".json")
)


@pytest.mark.parametrize("grid_name", GRID_FILES, ids=GRID_FILES)
def test_hepi_fast_plot_for_all_packaged_grids(grid_name, monkeypatch, tmp_path):
    output_path = tmp_path / f"{Path(grid_name).stem}.png"

    plt.close("all")
    monkeypatch.setattr(plt, "show", lambda: None)
    monkeypatch.setattr(
        sys,
        "argv",
        ["hepi-fast", grid_name, "--plot", "--output", str(output_path)],
    )

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            main()

        figures = [plt.figure(num) for num in plt.get_fignums()]
        assert figures, f"Expected {grid_name} to create at least one figure."
        assert any(fig.axes for fig in figures), (
            f"Expected {grid_name} to create at least one populated figure."
        )
        assert output_path.exists(), f"Expected {grid_name} to write {output_path}."
        assert output_path.stat().st_size > 0, (
            f"Expected {grid_name} to write a non-empty plot file."
        )
    finally:
        plt.close("all")
