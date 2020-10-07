# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from typing import List, Literal
from tqdm import tqdm


# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------


def parse_data(csv_file: Path, bof_bytes: int) -> pd.DataFrame:
    df = pd.read_csv(csv_file)
    bof = df["path"].map(lambda p: Path(p).read_bytes().hex()[:bof_bytes])
    df["bof"] = bof
    return df


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main() -> None:
    data_path: Path = Path(__file__).parent.resolve() / "data"
    df_123: pd.DataFrame = parse_data(data_path / "123_files.csv", 16)
    grouped_123 = df_123.groupby("bof")["id"].count()
    plt.figure()
    grouped_123.plot.bar()
    plt.show()


if __name__ == "__main__":
    main()
