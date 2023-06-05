"""This module contains functions used for input parsing.
"""
import functools
import re

import ase
import ase.io
import joblib
import pandas as pd

__all__ = ["get_comments_df", "read_raw_data", "parse_feature_name"]


def parse_feature_name(feature_signature: str) -> dict[str, tuple]:
    """Parses feature name into dict that store function alias
        and atoms idxs that were used in feature generation.

    Args:
        feature_name (str): Name of feature.

    Returns:
        dict[str, tuple]: dict with two keys:
            alias store feature name
            atoms_idxs store idxs used in feature generation.
    """
    args = re.findall(r"\d+", feature_signature)
    feature_alias = re.match(r"^[a-z_]+", feature_signature).group()
    return {
        "signature": feature_signature,
        "alias": feature_alias,
        "atoms_idxs": tuple(int(arg) for arg in args)
    }

def read_raw_data(
    particles_path: str, transports_path: str, cache_path: str
) -> pd.DataFrame:
    """Reads data from cache file or create it by itself.

    Args:
        particles_path (str): Path to .xyz file with atoms definitions.
        transports_path (str): Path to .trans file.
        cache_path (str): Path where parsed data will be stored for future runs

    Returns:
        pd.DataFrame: Data frame with two columns: 'obj', 'y'.
            obj contains ase.Atoms object and y floats from 0 to 1.
    """
    @joblib.Memory(cache_path).cache
    def cached_reader(particles_path, transport_path):
        return pd.DataFrame({
                "obj": ase.io.iread(particles_path),
                "y": pd.read_csv(transport_path, header=None)[0],
        })
    return cached_reader(particles_path, transports_path)

@functools.cache
def get_comments_df(file_path: str) -> pd.DataFrame:
    """Load and parse xyz file. This is not general purpose function!
    It is designed to work with xyz file that contains:
    Atoms with 42 positions and comments in format:
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

    with open(path, encoding="utf-8") as f:
        for line in f:
            if next_line_is_comment:
                comments.append(line.strip())
            next_line_is_comment = line == specified_line
    return comments


def main():
    print(parse_feature_name("dstC12C1"))
    print(parse_feature_name("angC2Au11Au1"))
    print(parse_feature_name("benzene_distance"))

if __name__ == "__main__":
    main()
