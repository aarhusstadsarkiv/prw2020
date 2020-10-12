# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from matplotlib.axes import Axes
from typing import List

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------


def add_vertical_value_labels(ax: Axes, spacing: int = 5) -> None:
    """Add labels to the end of each bar in a bar chart."""

    # For each bar: Place a label
    for rect in ax.patches:
        # Get X and Y placement of label from rect.
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2

        # Number of points between bar and label. Change to your liking.
        space = spacing
        # Vertical alignment for positive values
        va = "bottom"

        # If value of bar is negative: Place label below bar
        if y_value < 0:
            # Invert space to place label below
            space *= -1
            # Vertically align label at top
            va = "top"

        label = f"{y_value}"
        # Create annotation
        ax.annotate(
            label,  # Use `label` as label
            (x_value, y_value),  # Place label at end of the bar
            xytext=(0, space),  # Vertically shift label by space
            textcoords="offset points",  # Interpret xytext as offset in points
            ha="center",  # Horizontally center label
            va=va,  # Vertically align label differently
            fontsize=8,
        )


def add_horizontal_value_labels(ax: Axes, spacing: float = 5) -> None:
    """Add labels to the end of each bar in a bar chart."""

    # For each bar: Place a label
    for rect in ax.patches:
        # Get X and Y placement of label from rect.
        x_value = rect.get_width()
        y_value = rect.get_y() + rect.get_height() / 2

        # Number of points between bar and label. Change to your liking.
        space = spacing
        # Vertical alignment for positive values
        ha = "left"

        # If value of bar is negative: Place label below bar
        if x_value < 0:
            # Invert space to place label below
            space *= -1
            # Horizontally align label at right
            ha = "right"

        label = f"{x_value}"
        # Create annotation
        ax.annotate(
            label,  # Use `label` as label
            (x_value, y_value),  # Place label at end of the bar
            xytext=(space, 0),  # Vertically shift label by space
            textcoords="offset points",  # Interpret xytext as offset in points
            ha=ha,  # Horizontally center label
            va="center",  # Vertically align label differently
            fontsize=8,
        )