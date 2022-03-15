import pandas as pd
import seaborn as sns
from scipy.stats import zscore


def zscore_heatmap(
    dataframe: pd.DataFrame, index: str = None, head: int = None, abs: bool = None, return_dataframe: bool = False
):
    """The z-score also know as standard score is the number of standard
    deviations by which the value of a raw score is above or below the mean and
    can be used to analyse how deviant an observation is from the rest of the
    distribution.

    This function provides not only z-score for the given dataframe but also
    presents it in the form of a heatmap.

        Args:
            **df** (pandas.DataFrame): The dataframe to be transformed

            **index** (str): The index of the dataframe e.g. the datetime of
            each row.

            **max** (int): The number of rows to be presented in the heatmap.

            **abs** (bool): Present only abosulte values.

            **return_dataframe** (bool): The possibility of returning the
            zscore dataframe or only presenting the heatmap.

        Returns:
            (pd.Dataframe): Transformed dataframe"""

    heatmap_df = dataframe.copy(deep=True)
    if index:
        heatmap_df.set_index(index, inplace=True)

    heatmap_df = heatmap_df.apply(zscore)

    if abs:
        heatmap_df = heatmap_df.abs()

    if head:
        heatmap_df = heatmap_df.head(head)

    sns.heatmap(heatmap_df, annot=True)
    if return_dataframe:
        return heatmap_df

    del heatmap_df


def visualize_oam_results(result_df, head):
    # a set will avoid duplication when adding new dimensions to it
    subspace = set(result_df.loc[0].subspace)
    # add every dimension found
    for dimension in result_df.subspace[1:]:
        for dimension in dimension:
            subspace.add(dimension)

    viz_df = pd.DataFrame(columns=subspace)

    # add a 1 in the dimension found in that subspace
    for idx, subspace in enumerate(result_df.subspace):
        for dimension in subspace:
            viz_df.loc[idx, dimension] = 1
    viz_df.fillna(0, inplace=True)

    # add the score correspondent to that subspace
    for idx, score in enumerate(result_df.score):
        viz_df.loc[idx, "score"] = score

    viz_df = viz_df.head(head)
    sns.heatmap(viz_df, annot=True)
