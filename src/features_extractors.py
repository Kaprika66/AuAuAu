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

# Dataframe manipulators


def add_angle_feature(df: pd.DataFrame, idx1, idx2, idx3):
    particle = df.loc[0, "obj"]
    feature_name = f"ang{generate_feature_id(particle, idx1, idx2, idx3)}"
    df[feature_name] = df["obj"].apply(lambda p: p.get_angle(idx1, idx2, idx3))


def add_dihedral_feature(df: pd.DataFrame, idx1, idx2, idx3, idx4):
    particle = df.loc[0, "obj"]
    feature_name = f"dih{generate_feature_id(particle, idx1, idx2, idx3, idx4)}"
    df[feature_name] = df["obj"].apply(lambda p: p.get_dihedral(idx1, idx2, idx3, idx4))


def add_dst_feature(df: pd.DataFrame, idx1, idx2):
    particle = df.loc[0, "obj"]
    feature_name = f"dst{generate_feature_id(particle, idx1, idx2)}"
    df[feature_name] = df["obj"].apply(lambda p: p.get_distance(idx1, idx2))


# Particle manipulators


def get_benzine_dst(particle: ase.atoms.Atoms, benzene1_idxes, benzene2_idxes):
    benzene1_center = np.mean(particle.positions[benzene1_idxes], axis=0)
    benzene2_center = np.mean(particle.positions[benzene2_idxes], axis=0)
    return np.linalg.norm(benzene1_center - benzene2_center)


def angle_between_planes(particle: ase.atoms.Atoms, plane1_idxes, plane2_idxes):
    normal_vec1 = calculate_normal_vector(particle, plane1_idxes)
    normal_vec2 = calculate_normal_vector(particle, plane2_idxes)
    return angle_between(normal_vec1, normal_vec2)


def calculate_normal_vector(particle: ase.atoms.Atoms, plane_idxes):
    idx_0, idx_1, idx_2 = plane_idxes
    v1 = particle.positions[idx_0] - particle.positions[idx_1]
    v2 = particle.positions[idx_2] - particle.positions[idx_1]
    return np.cross(v1, v2)


def get_particle_symbols(particle: ase.atoms.Atoms, *idxes):
    return [particle.get_chemical_symbols()[idx] for idx in idxes]


def generate_feature_id(particle: ase.atoms.Atoms, *idxes):
    symbols = get_particle_symbols(particle, *idxes)
    return "".join([f"{s}{idx}" for s, idx in zip(symbols, idxes)])


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
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
