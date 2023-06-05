"""Module with complex plots definitions.
"""


import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd


def draw_correlation_matrix(corr_matrix: pd.DataFrame, ax: mpl.axes.Axes):
    """Draw correlation matrix on given axis.

    Args:
        corr_matrix (pd.DataFrame): Correlation matrix - it don't need to be square.
        ax (mpl.axes.Axes): matplotlib axes object.

    Example:
        corr_matrix = df.corr(numeric_only=False)
        fig, ax = plt.subplots()
        visualization.draw_correlation_matrix(corr_matrix, ax)
        plt.show()
    """
    col_num = len(corr_matrix.columns)
    row_num = len(corr_matrix.index)

    # plot a heatmap of the correlation matrix
    im = ax.imshow(corr_matrix.values, cmap="coolwarm")

    # add the column names as tick labels
    ax.set_xticks(range(col_num))
    ax.set_yticks(range(row_num))
    ax.set_xticklabels(corr_matrix.columns, rotation=90)
    ax.set_yticklabels(corr_matrix.index)

    plt.grid(False)

    # add the correlation coefficients as text annotations
    for i in range(row_num):
        for j in range(col_num):
            ax.text(
                j,
                i,
                round(corr_matrix.values[i, j], 2),
                ha="center",
                va="center",
                color="black",
            )

    # add a color bar
    ax.figure.colorbar(im, ax=ax)

    # set the title and show the plot
    ax.set_title("Correlation Heatmap")
