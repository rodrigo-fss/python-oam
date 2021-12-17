import pytest

import pandas as pd

from oam.preprocess import normalize


@pytest.fixture
def dataframe():
    df = pd.read_csv('../../datasets/df_outliers.csv')
    df = df[
        ['variation_mean', 'variation_std',	'up_count',
         'down_count', 'top_15_variation_mean', 'top_15_variation_std']
    ]

    return df


def test_normalization(dataframe):
    df = normalize(dataframe, 0, 5)
    assert all([min == 0 for min in df.min()])
    assert all([max == 5 for max in df.max()])
