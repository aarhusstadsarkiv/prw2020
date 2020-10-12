# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import List, Literal
from tqdm import tqdm
from matplotlib import rcParams
from prw.plot_utils import add_horizontal_value_labels

## Matplotlib params
rcParams["axes.facecolor"] = "#e9e9e9"
rcParams.update({"figure.autolayout": True})
rcParams.update({"axes.axisbelow": True})


# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------


def parse_data(csv_file: Path, bof_bytes: int) -> pd.DataFrame:
    df = pd.read_csv(csv_file)
    bof = df["path"].map(lambda p: Path(p).read_bytes().hex()[:bof_bytes])
    df["bof"] = bof
    return df


def bar_plot_df(df: pd.DataFrame, title: str, save_to: Path) -> None:
    plt.figure()
    ax = df.plot.barh(grid=True, color="seagreen")
    # Axes
    ax.grid(color="white")
    if "123" in title:
        ax.set_xlim(0, df.max() + 10)
    elif "LWP" in title:
        ax.set_xlim(0, df.max() + 10)
    # Title & labels
    plt.title(title)
    add_horizontal_value_labels(ax, spacing=0.5)
    plt.xlabel("Count")

    plt.tight_layout()
    plt.savefig(save_to)
    plt.clf()


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main() -> None:
    data_path: Path = Path(__file__).parent.resolve() / "data"
    plot_path: Path = Path(__file__).parent.resolve() / "plots"
    df_123: pd.DataFrame = parse_data(data_path / "open_123_files.csv", 16)
    grouped_123 = df_123.groupby("bof")["id"].count()
    bar_plot_df(
        grouped_123,
        "123 File Signatures",
        save_to=plot_path / "open_123_plot.png",
    )
    df_lwp: pd.DataFrame = parse_data(data_path / "open_lwp_files.csv", 64)
    df_lwp = df_lwp[df_lwp.puid == "x-fmt/340"]
    grouped_lwp = df_lwp.groupby("bof")["id"].count()
    new_index = [f"[...]{index[-4:]}" for index in list(grouped_lwp.index)]
    grouped_lwp.index = pd.Index(new_index, name="bof")
    bar_plot_df(
        grouped_lwp,
        "LWP x-fmt 340 File Signatures",
        save_to=plot_path / "open_lwp_plot.png",
    )


if __name__ == "__main__":
    main()
