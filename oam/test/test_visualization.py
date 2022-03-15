import pandas as pd
import pytest

from oam.score.isolation_path import IsolationPath
from oam.search.simple_combination import SimpleCombination
from oam.visualization import visualize_oam_results, zscore_heatmap


@pytest.fixture
def dataframe():
    df = pd.read_csv("datasets/df_outliers.csv")
    df = df.sort_values(by=["LOF_score"])
    df = df[
        [
            "datetime",
            "variation_mean",
            "variation_std",
            "up_count",
            "down_count",
            "top_15_variation_mean",
            "top_15_variation_std",
        ]
    ]

    return df


@pytest.fixture
def ipath_result_df():
    df = pd.read_csv("datasets/df_outliers.csv")
    ipath = IsolationPath(subsample_size=256, number_of_paths=10)
    search = SimpleCombination(
        ipath,
        min_items_per_subspace=2,
        max_items_per_subspace=4,
        dimensions=[
            "variation_mean",
            "variation_std",
            "up_count",
            "down_count",
            "top_15_variation_mean",
            "top_15_variation_std",
        ],
    )
    result_df = search.search(df, 41)
    return result_df


def test_zscore_heatmap(dataframe):
    zscore_heatmap(dataframe, index="datetime", head=5, abs=True)
    assert True


def test_oam_result_visualization(ipath_result_df):
    visualize_oam_results(ipath_result_df, 5)
    assert True
