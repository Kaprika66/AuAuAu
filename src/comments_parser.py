"""This module contains functions used for comments parsing.
"""

import pandas as pd

__all__ = ["get_comments_df"]


def get_comments_df(file_path: str) -> pd.DataFrame:
    """Load and parse xyz file. This is not general purpose function!
    It is designed to work with xyz file that contains:
    All atoms with 42 positions and comments in format:
        - id
        - total energy
        - fermi energy
        - unimportant '1'
        - 136 energy levels
        - 150 electron states
    Args:
        file_path (str): path to xyz file to parse.

    Returns:
        pd.DataFrame: Datframe with parsed comments in rows
            and columns identical as in the list above.
    """
    comments = _load_lines_after_specified_one(file_path, "42\n")
    comments_df = pd.Series(comments).str.split(expand=True).astype(float)

    column_names = (
        ["id", "total_energy", "fermi_energy", "1"]
        + [f"energy_level_{i}" for i in range(140 - 4)]
        + [f"electron_state_{i}" for i in range(len(comments_df.columns) - 140)]
    )
    comments_df.columns = column_names
    return comments_df


def _load_lines_after_specified_one(path: str, specified_line: str) -> list[str]:
    comments = []
    next_line_is_comment = False

    with open(path) as f:
        for line in f:
            if next_line_is_comment:
                comments.append(line.strip())
            next_line_is_comment = line == specified_line
    return comments
