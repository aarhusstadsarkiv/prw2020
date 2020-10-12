# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import List, Literal
from tqdm import tqdm
from matplotlib import rcParams
from prw.plot_utils import add_horizontal_value_labels, add_vertical_value_labels

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


def barh_plot_df(df: pd.DataFrame, title: str, save_to: Path) -> None:
    plt.figure()
    ax = df.plot.barh(grid=True, color="seagreen")
    # Axes
    ax.grid(color="white")
    # if "123" in title:
    #     ax.set_xlim(0, df.max() + 50)
    # elif "LWP" in title:
    #     ax.set_xlim(0, df.max() + 10)
    # Title & labels
    plt.title(title)
    add_horizontal_value_labels(ax, spacing=0.5)
    plt.xlabel("Count")

    plt.tight_layout()
    plt.savefig(save_to)
    plt.clf()

def bar_plot_df(df: pd.DataFrame, title: str, save_to: Path) -> None:
    plt.figure()
    ax = df.plot.bar(grid=True, rot=45)
    # Axes
    ax.grid(color="white")
    # if "123" in title:
    #     ax.set_xlim(0, df.max() + 50)
    # elif "LWP" in title:
    #     ax.set_xlim(0, df.max() + 10)
    # # Title & labels
    plt.title(title)
    # add_vertical_value_labels(ax, spacing=0.5)
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
    # file_info = []
    # linux_123: pd.DataFrame = pd.read_csv(data_path / "123_df.csv")
    # for row in linux_123.itertuples():
    #     result = subprocess.run(["wslpath", row.path], capture_output=True)
    #     linux_path = Path(result.stdout.decode().strip())
    #     file_result = subprocess.run(["file", "-b", linux_path], capture_output=True)
    #     file_stdout = file_result.stdout.decode().strip()
    #     file_str= "".join(file_stdout.split(",")[:2])
    #     file_str=file_str.title()
    #     if "Targa" in file_str:
    #         file_str = "Targa Image Data"
    #     file_info.append(file_str)
    # linux_123["file_info"] = file_info
    # linux_123.to_csv(data_path/"123_df_updated.csv")
    updated_123_df = pd.read_csv(data_path/"123_df_updated.csv")
    grouped = updated_123_df.groupby(['bof', 'file_info'])["id"].count().unstack("bof")
    new_index = []
    for inx in grouped.index:
        if "Unknown" in inx:
            new_index.append("Unknown")
        if "9.8" in inx:
            new_index.append("Version 9.8")
        if "97" in inx:
            new_index.append("Version 97")
        if "Targa" in inx:
            new_index.append("Targa Image")
    grouped.index = pd.Index(new_index, name="file_info")
    bar_plot_df(grouped, "123 Signatures & File Information", save_to=plot_path/"123_group.png")
        
    # print(linux_123)
    # plot_path: Path = Path(__file__).parent.resolve() / "plots"
    # df_123: pd.DataFrame = parse_data(data_path / "123_files.csv", 16)
    # df_123 = df_123[df_123.puid == "aca-fmt/1"]
    # df_123.to_csv(data_path / "test.csv", index=False)
    # grouped_123 = df_123.groupby("bof")["id"].count()
    # bar_plot_df(
    #     grouped_123,
    #     "123 File Signatures",
    #     save_to=plot_path / "123_plot.png",
    # )

    # for row in df_123.itertuples():
    #     print(Path(row.path))

    # df_lwp: pd.DataFrame = parse_data(data_path / "open_lwp_files.csv", 64)
    # df_lwp = df_lwp[df_lwp.puid == "x-fmt/340"]
    # grouped_lwp = df_lwp.groupby("bof")["id"].count()
    # new_index = [f"[...]{index[-4:]}" for index in list(grouped_lwp.index)]
    # grouped_lwp.index = pd.Index(new_index, name="bof")
    # bar_plot_df(
    #     grouped_lwp,
    #     "LWP x-fmt 340 File Signatures",
    #     save_to=plot_path / "open_lwp_plot.png",
    # )


if __name__ == "__main__":
    main()
