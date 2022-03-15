import sys

import pandas as pd
import seaborn as sns
from scipy import stats

sys.path.insert(0, "../../")
from oam.score.isolation_path import IsolationPath
from oam.search.simple_combination import SimpleCombination

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)

df = pd.read_csv("../../datasets/df_outliers.csv")
distance = pd.DataFrame()
correlation_list = []

for number_of_paths in range(1500, 100, -100):
    ipath = IsolationPath(subsample_size=256, number_of_paths=number_of_paths)

    search = SimpleCombination(
        ipath,
        min_items_per_subspace=3,
        max_items_per_subspace=3,
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
    result_df.reset_index(drop=True, inplace=True)
    distance[number_of_paths] = result_df.score

distance = distance * 100
perfect_score = list(distance[1500])


def _spearmanr(column):
    return stats.spearmanr(perfect_score, list(column))[0]


def _pearsonr(column):
    return stats.pearsonr(perfect_score, list(column))[0]


correlation_df = distance.apply(_spearmanr, axis=0)
sns.scatterplot(data=correlation_df)

correlation_df = distance.apply(_pearsonr, axis=0)
sns.scatterplot(data=correlation_df)
