import pandas as pd


def normalize(df: pd.DataFrame, min: int, max: int, weights: dict = None) -> pd.DataFrame:
    """A min-max normalization to all the columns in the dataframe.
    If desired you can change the scale of a given column using the 'weights'
    param. The weight will be multiplied by every value in the column, given it
    more or less importance in the model to be used.

    Args:
        df (pandas.DataFrame): The dataframe to be transformed.

        min (int): The lower limit of the feature' new range.

        max (int): The upper limit of the feature's new range.

        weights (dict): Key should be the column name and value
            should be the weight that will multiply it's values.

    Returns:
        (pd.Dataframe): Transformed dataframe."""

    normalized_df = (df - df.min()) / (df.max() - df.min())
    X_scaled = normalized_df * (max - min) + min

    if weights:
        for column, weight in weights.items():
            df[column] = df[column] * weight

    return X_scaled
