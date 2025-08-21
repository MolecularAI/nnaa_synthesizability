import os
from typing import Union, List

import pandas as pd
from rxnutils.chem.features.sc_score import SCScore
from rxnutils.routes.base import SynthesisRoute
from rxnutils.routes.deepset.scoring import deepset_route_score, DeepsetModelClient
from rxnutils.routes.scoring import (
    reaction_feasibility_score,
    ChemformerReactionFeasibilityCalculator,
)

class FeasibilityScorer:

    def __init__(self, chemformer_url=None, path_expert_augmented=None):
        self._api_url = chemformer_url
        if self._api_url:
            self._chemformer = ChemformerReactionFeasibilityCalculator(self._api_url)

        self._path_expert_augmented = path_expert_augmented
        if self._path_expert_augmented:
            df = pd.read_csv(os.path.join(self._path_expert_augmented, "reaction_class_ranks.csv"), sep=",")
            self._reaction_class_ranks = dict(zip(df["reaction_class"], df["rank_score"]))
            self._scscorer = SCScore(os.path.join(self._path_expert_augmented, "scscore_model_1024_bits.onnx"))
            self._deepset_client = DeepsetModelClient(os.path.join(self._path_expert_augmented, "deepset_route_scoring_sdf.onnx"))

    def score_with_chemformer(self, route: SynthesisRoute) -> float:
        score = reaction_feasibility_score(route, self._chemformer)
        return score

    def score_with_expert_augmented_feasibility(self, route: SynthesisRoute, chemformer_score: Union[float, None] = None) -> float:
        if chemformer_score==0.0:
            score = 20.0
        else:
            score = deepset_route_score(route, self._deepset_client, self._scscorer, self._reaction_class_ranks)
        return score