import pytest

import pandas as pd

from oam.score.isolation_path import IsolationPath
from oam.search.simple_combination import SimpleCombination


@pytest.fixture
def dataframe():
    return pd.read_csv('../../datasets/df_outliers.csv')


@pytest.fixture
def ipath():
    return IsolationPath(
        subsample_size=50,
        number_of_paths=5
    )


@pytest.fixture
def ipath_sc(ipath):
    return SimpleCombination(
        ipath,
        min_items_per_subspace=2,
        max_items_per_subspace=3,
        dimensions=['variation_mean', 'variation_std', 'up_count',
                    'down_count', 'top_15_variation_mean',
                    'top_15_variation_std'],
    )


@pytest.fixture
def sc_defined_subspaces(ipath):
    return SimpleCombination(
        ipath,
        subspaces=[
            ['variation_std', 'down_count', 'top_15_variation_std'],
            ['variation_mean', 'up_count', 'top_15_variation_mean']
        ]
    )


def test_generate_subspaces(ipath_sc):
    subspaces = ipath_sc._generate_subspaces()
    expected_subspaces = [
        ['variation_mean', 'variation_std'],
        ['variation_mean', 'up_count'],
        ['variation_mean', 'down_count'],
        ['variation_mean', 'top_15_variation_mean'],
        ['variation_mean', 'top_15_variation_std'],
        ['variation_std', 'up_count'],
        ['variation_std', 'down_count'],
        ['variation_std', 'top_15_variation_mean'],
        ['variation_std', 'top_15_variation_std'],
        ['up_count', 'down_count'],
        ['up_count', 'top_15_variation_mean'],
        ['up_count', 'top_15_variation_std'],
        ['down_count', 'top_15_variation_mean'],
        ['down_count', 'top_15_variation_std'],
        ['top_15_variation_mean', 'top_15_variation_std'],
        ['variation_mean', 'variation_std', 'up_count'],
        ['variation_mean', 'variation_std', 'down_count'],
        ['variation_mean', 'variation_std', 'top_15_variation_mean'],
        ['variation_mean', 'variation_std', 'top_15_variation_std'],
        ['variation_mean', 'up_count', 'down_count'],
        ['variation_mean', 'up_count', 'top_15_variation_mean'],
        ['variation_mean', 'up_count', 'top_15_variation_std'],
        ['variation_mean', 'down_count', 'top_15_variation_mean'],
        ['variation_mean', 'down_count', 'top_15_variation_std'],
        ['variation_mean', 'top_15_variation_mean', 'top_15_variation_std'],
        ['variation_std', 'up_count', 'down_count'],
        ['variation_std', 'up_count', 'top_15_variation_mean'],
        ['variation_std', 'up_count', 'top_15_variation_std'],
        ['variation_std', 'down_count', 'top_15_variation_mean'],
        ['variation_std', 'down_count', 'top_15_variation_std'],
        ['variation_std', 'top_15_variation_mean', 'top_15_variation_std'],
        ['up_count', 'down_count', 'top_15_variation_mean'],
        ['up_count', 'down_count', 'top_15_variation_std'],
        ['up_count', 'top_15_variation_mean', 'top_15_variation_std'],
        ['down_count', 'top_15_variation_mean', 'top_15_variation_std']
    ]
    assert subspaces == expected_subspaces


def test_ipath_scoring(ipath_sc, dataframe):
    score_output = ipath_sc.search(dataframe, 41)
    assert score_output.shape == (35, 3)


def test_ipath_defined_subspaces(sc_defined_subspaces, dataframe):
    score_output = sc_defined_subspaces.search(dataframe, 41)
    assert score_output.shape == (2, 3)
