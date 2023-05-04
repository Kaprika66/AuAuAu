"""This module contains methods that calculate geometric features based on
ASE.atoms objects. It is divided into few segments sorted by importance:

Dataframe manipulators:
Have 'df' input parameter that is Pandas dataframe with column named 'obj'
which contains ASE.atoms objects. Module functions modify dataframe directly
by adding new feature to it. They don't return anything.

Particle manipulators:
Contains functions that are base for dataframe manipulators.
You can use it directly to calculate features for single particle if you want.

Lin. alg. helpers:
Contains linear algebra functions that I wasn't able to find in ASE.atoms documentation.
"""

import ase.atoms
import numpy as np
import pandas as pd

import src.function_manipulators as function_manipulators

# Dataframe manipulators


def __check_df(df: pd.DataFrame):
    if not isinstance(df, pd.DataFrame):
        raise ValueError("df should be pandas DataFrame object.")

    if "obj" not in df.columns:
        raise ValueError("df not contain 'obj' column.")

    if len(df["obj"]) < 1:
        raise ValueError("'obj' column need at least one element but it is empty")

    are_atoms_type = df["obj"].apply(lambda x: isinstance(x, ase.atoms.Atoms))
    if not np.all(are_atoms_type):
        raise ValueError("Elements of 'obj' column should be ase.atoms.Atoms type")


@function_manipulators.assert_proper_input("df", __check_df)
def add_ang_feature(df: pd.DataFrame, idx1, idx2, idx3):
    """Calculate angle between three atoms and append it to dataframe
    as column with name starts with ang.

    Args:
        df (pd.DataFrame): df with ase.Atoms column named 'obj'
        idx1 (int): atom index
        idx2 (int): atom index
        idx3 (int): atom index
    """
    __add_universal_feature(
        df,
        ase.Atoms.get_angle,
        "ang",
        *(idx1, idx2, idx3),
    )


@function_manipulators.assert_proper_input("df", __check_df)
def add_dih_feature(df: pd.DataFrame, idx1, idx2, idx3, idx4):
    """Calculate dihedral angle between four atoms and append it to dataframe
    as column with name starts with dih.

    Args:
        df (pd.DataFrame): df with ase.Atoms column named 'obj'
        idx1 (int): atom index
        idx2 (int): atom index
        idx3 (int): atom index
        idx4 (int): atom index
    """
    __add_universal_feature(
        df,
        ase.Atoms.get_dihedral,
        "dih",
        *(idx1, idx2, idx3, idx4),
    )


@function_manipulators.assert_proper_input("df", __check_df)
def add_dst_feature(df: pd.DataFrame, idx1, idx2):
    """Calculate distance between two atoms and append it to dataframe
    as column with name starts with dst.

    Args:
        df (pd.DataFrame): DataFrame with column 'obj' containing ase.Atoms obj
        idx1 (int): index of atom
        idx2 (int): index of atom
    """
    __add_universal_feature(
        df,
        ase.Atoms.get_distance,
        "dst",
        *(idx1, idx2),
    )


@function_manipulators.assert_proper_input("df", __check_df)
def add_benzene_dst_feature(df: pd.DataFrame, benzene1_idxs, benzene2_idxs):
    """Calculate distance between benzenes
        and add it to dataframe as column with name benzene_dst

    Args:
        df (pd.DataFrame): _description_
        benzene1_idxs (tuple[int*6]): all indexes of first benzene
        benzene2_idxs (tuple[int*6]): all indexes of second benzene
    """
    df["benzene_dst"] = df["obj"].apply(
        lambda p: get_benzene_dst(p, benzene1_idxs, benzene2_idxs)
    )


@function_manipulators.assert_proper_input("df", __check_df)
def add_benzene_cossq_feature(df: pd.DataFrame, benzene1_idxs, benzene2_idxs):
    """Calculate cossinus square of benzene twist angle
        and add it to dataframe as column with name benzene_cossq

    Args:
        df (pd.DataFrame): DataFrame with column 'obj' containing ase.Atoms obj
        benzene1_idxs (tuple[int, int, int]): Three indices from benzene.
        benzene2_idxs (tuple[int, int, int]): Three indices from benzene.
    """
    df["benzene_cossq"] = df["obj"].apply(
        lambda p: cos_between_planes(p, benzene1_idxs, benzene2_idxs) ** 2
    )


def __add_universal_feature(df, func, name_prefix: str, *idxs):
    particle = df.loc[0, "obj"]
    feature_name = f"{name_prefix}{generate_feature_id(particle, *idxs)}"
    df[feature_name] = df["obj"].apply(lambda p: func(p, *idxs))


def add_comment_feature(
    df: pd.DataFrame, comment_df: pd.DataFrame, feature: str
) -> None:
    """

    Args:
        df (pd.DataFrame): _description_
        comment_df (pd.DataFrame): _description_
        feature (str): _description_
    """
    df[feature] = comment_df[feature]


# Particle manipulators


def get_benzene_dst(particle: ase.atoms.Atoms, benzene1_idxs, benzene2_idxs):
    benzene1_center = np.mean(particle.positions[benzene1_idxs], axis=0)
    benzene2_center = np.mean(particle.positions[benzene2_idxs], axis=0)
    return np.linalg.norm(benzene1_center - benzene2_center)


def cos_between_planes(particle: ase.atoms.Atoms, plane1_idxs, plane2_idxs):
    normal_vec1 = calculate_perpendicular_vector(particle, plane1_idxs)
    normal_vec2 = calculate_perpendicular_vector(particle, plane2_idxs)
    return cos_between(normal_vec1, normal_vec2)


def calculate_perpendicular_vector(particle: ase.atoms.Atoms, plane_idxs):
    idx_0, idx_1, idx_2 = plane_idxs
    v1 = particle.positions[idx_0] - particle.positions[idx_1]
    v2 = particle.positions[idx_2] - particle.positions[idx_1]
    return np.cross(v1, v2)


def get_particle_symbols(particle: ase.atoms.Atoms, *idxs):
    return [particle.get_chemical_symbols()[idx] for idx in idxs]


def generate_feature_id(particle: ase.atoms.Atoms, *idxs, prefix: str = ""):
    symbols = get_particle_symbols(particle, *idxs)
    return prefix + "".join([f"{s}{idx}" for s, idx in zip(symbols, idxs)])


# Lin. alg. helpers


def unit_vector(vector):
    """Returns the unit vector of the vector."""
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    """Returns the angle in radians between vectors 'v1' and 'v2'::

    >>> angle_between((1, 0, 0), (0, 1, 0))
    1.5707963267948966
    >>> angle_between((1, 0, 0), (1, 0, 0))
    0.0
    >>> angle_between((1, 0, 0), (-1, 0, 0))
    3.141592653589793
    """
    cos = cos_between(v1, v2)
    return cos_to_angle(cos)


def cos_between(v1, v2):
    """Returns the cossinus between vectors 'v1' and 'v2'::"""
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.dot(v1_u, v2_u)


def cos_to_angle(cos):
    return np.arccos(np.clip(cos, -1.0, 1.0))
