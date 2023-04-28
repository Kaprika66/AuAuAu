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
import joblib
import numpy as np
import pandas as pd

import src.function_manipulators as function_manipulators

# Dataframe manipulators

def __check_df(df):
    if not isinstance(df, pd.DataFrame):
        raise ValueError("df should be pandas DataFrame object.")

    if 'obj' not in df.columns:
        raise ValueError("df not contain 'obj' column.")

    if len(df['obj']) < 1:
        raise ValueError("'obj' column need at least one element but it is empty")

    are_atoms_type = df['obj'].apply(lambda x: isinstance(x, ase.atoms.Atoms))
    if not np.all(are_atoms_type):
        raise ValueError("Elements of 'obj' column should be ase.atoms.Atoms type")


@function_manipulators.assert_proper_input("df", __check_df)
def add_angle_feature(df: pd.DataFrame, idx1, idx2, idx3):
    particle = df.loc[0, "obj"]
    feature_name = f"ang{generate_feature_id(particle, idx1, idx2, idx3)}"
    df[feature_name] = df["obj"].apply(lambda p: p.get_angle(idx1, idx2, idx3))


@function_manipulators.assert_proper_input("df", __check_df)
def add_dihedral_feature(df: pd.DataFrame, idx1, idx2, idx3, idx4):
    particle = df.loc[0, "obj"]
    feature_name = f"dih{generate_feature_id(particle, idx1, idx2, idx3, idx4)}"
    df[feature_name] = df["obj"].apply(lambda p: p.get_dihedral(idx1, idx2, idx3, idx4))


@function_manipulators.assert_proper_input("df", __check_df)
def add_dst_feature(df: pd.DataFrame, idx1, idx2):
    particle = df.loc[0, "obj"]
    feature_name = f"dst{generate_feature_id(particle, idx1, idx2)}"
    # dst = joblib.delayed(lambda p: p.get_distance(idx1, idx2))
    # df[feature_name] = joblib.Parallel(
    #     n_jobs=-1)(dst(p) for p in df["obj"]
    # )
    df[feature_name] = df["obj"].apply(lambda p: p.get_distance(idx1, idx2))


@function_manipulators.assert_proper_input("df", __check_df)
def add_benzene_dst_feature(df: pd.DataFrame, benzene1_idxs, benzene2_idxs):
    df["benzene_dst"] = df["obj"].apply(
        lambda p: get_benzene_dst(p, benzene1_idxs, benzene2_idxs)
    )


@function_manipulators.assert_proper_input("df", __check_df)
def add_benzene_cossq_feature(df: pd.DataFrame, benzene1_idxs, benzene2_idxs):
    df["benzene_cossq"] = df["obj"].apply(
        lambda p: cos_between_planes(p, benzene1_idxs, benzene2_idxs)**2
    )


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


def generate_feature_id(particle: ase.atoms.Atoms, *idxs):
    symbols = get_particle_symbols(particle, *idxs)
    return "".join([f"{s}{idx}" for s, idx in zip(symbols, idxs)])


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
    """Returns the cossinus between vectors 'v1' and 'v2'::
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.dot(v1_u, v2_u)


def cos_to_angle(cos):
    return np.arccos(np.clip(cos, -1.0, 1.0))
