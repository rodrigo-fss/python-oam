import sys

import pandas as pd

sys.path.insert(0, "../")
from oam.score.isolation_path import IsolationPath
from oam.search.simple_combination import SimpleCombination
from oam.visualization import visualize_oam_results

df = pd.read_csv("../datasets/df_outliers.csv")

correlation_list = []

ipath = IsolationPath(subsample_size=256, number_of_paths=600)

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
visualize_oam_results(result_df, 5)
