import logging
from concurrent import futures
from functools import partial
from itertools import combinations

import pandas as pd
from tqdm import tqdm

from oam.score import ScoringBaseClass


class SimpleCombination:
    def __init__(
        self,
        score_method_instance: ScoringBaseClass,
        min_items_per_subspace: int = None,
        max_items_per_subspace: int = None,
        dimensions: list = None,
        subspaces: list = None,
        multiprocessing: bool = None,
    ):
        """A Class to generate subspaces by combining the dimensions within
        the defined range, it will combine without repetition all to all
        dimensions, each combination will be called a subspace.

        You can pass your own list of subspaces as well, just make sure
        to leave the min_items_per_subspace, max_items_per_subspace and
        dimensions parameters empty.

        With the subspaces in hands you will be able to search through them
        to find what's the ones with higher outliing score.

        Args:
            **score_method_instance** (ScoringClass): the instance
                of the scoring method that will be used to evaluete each
                subspace.

            **min_items_per_subspace** (int): the lower limit of the subspace
                lenght to be created.

            **max_items_per_subspace** (int): the upper limit of the subspace
                lenght to be created.

            **dimensions** (list): the list of the columns found in your
                dataframe that should be combined to created the subspaces
                to search from.

            **subspaces** (list): the list of subspaces to search from.
                **if you use this argument, min, max and dimensions arguments
                will be ignored.**

            *multiprocessing* (bool): The option to enable multiprocessing.
                It will require a higher availability of memory but will
                potentially decrease a lot the search time if you have
                the resources."""

        self.score_method_instance = score_method_instance
        self.min_items_per_subspace = min_items_per_subspace
        if max_items_per_subspace:
            self.max_items_per_subspace = max_items_per_subspace + 1
        self.dimension = dimensions
        self.subspaces = subspaces
        self.multiprocessing = multiprocessing

    def search(self, dataframe: pd.DataFrame, query_point: int) -> pd.DataFrame:
        """This function will loop through all the subspaces scoring them all
        using the chosen scoring method and will return an ordered dataframe
        with the dimensions followed by its score.

        Args:
            dataframe (pd.DataFrame): The dataframe to be analysed

            query_point (int): The index of the row (query) you want
                to analyse

        Returns:
            (pd.Dataframe): A sorted dataframe with each
            dimension followed by its score"""

        if not self.subspaces:
            self.subspaces = self._generate_subspaces()

        results = pd.DataFrame(columns=["subspace", "score", "subspace_size"])

        if not self.multiprocessing:
            with tqdm(total=len(self.subspaces)) as pbar:
                for subspace in self.subspaces:
                    result_row = self._score_subspace(subspace, query_point, dataframe)
                    # Appends to the last line of the dataframe
                    results.loc[len(results)] = result_row
                    pbar.update()

        else:
            # Defining default arguments to the function
            partial_score_subspace = partial(self._score_subspace, query_point=query_point, dataframe=dataframe)
            # Copying the dataframe to every process - possible memory leak
            with futures.ProcessPoolExecutor(max_workers=2) as executor:
                for result_row in executor.map(partial_score_subspace, self.subspaces):
                    # Appends to the last line of the dataframe
                    results.loc[len(results)] = result_row

        return results.sort_values(by=["score"])

    def _generate_subspaces(self) -> list:
        # Using simple combination - all to all for every legth from min to max range
        subspaces_list = []
        for boundary in range(self.min_items_per_subspace, self.max_items_per_subspace):
            [
                subspaces_list.append(list(all_combinations))
                for all_combinations in combinations(self.dimension, boundary)
            ]

        return subspaces_list

    def _score_subspace(self, subspace_dimensions: list, query_point: int, dataframe: pd.DataFrame) -> list:

        score = self.score_method_instance.score(dataframe[subspace_dimensions], query_point)
        logging.info(f"subspace {str(subspace_dimensions)} scored: {str(score)}")
        return [subspace_dimensions, score, len(subspace_dimensions)]
