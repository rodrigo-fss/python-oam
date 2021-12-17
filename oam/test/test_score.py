import pytest
import pandas as pd

from oam.score.isolation_path import IsolationPath


@pytest.fixture
def dataframe():
    return pd.read_csv('../../datasets/df_outliers.csv')


@pytest.fixture
def ipath():
    return IsolationPath(
        subsample_size=50,
        number_of_paths=5
    )


def test_ipath_score(ipath, dataframe):
    subspace = ['variation_mean', 'variation_std', 'up_count', 'down_count']

    score = ipath.score(
        dataframe[subspace],
        41
    )
    assert isinstance(score, int) or isinstance(score, float)
