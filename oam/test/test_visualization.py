import pytest

import pandas as pd

from oam.visualization import zscore_heatmap


@pytest.fixture
def dataframe():
    df = pd.read_csv('../../datasets/df_outliers.csv')
    df = df.sort_values(by=['LOF_score'])
    df = df[
        ['datetime', 'variation_mean', 'variation_std',	'up_count',
         'down_count', 'top_15_variation_mean', 'top_15_variation_std']
    ]

    return df


def test_zscore_heatmap(dataframe):
    zscore_heatmap(
        dataframe,
        index='datetime',
        head=5,
        abs=True
    )
    assert True
