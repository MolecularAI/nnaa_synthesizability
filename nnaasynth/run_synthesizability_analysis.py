from typing import List

from rxnutils.routes.base import SynthesisRoute

from nnaasynth.dtos.aminoacid_dto import AminoAcidDTO
from nnaasynth.workflow_components.protection import Protection
from nnaasynth.dtos.result_dto import AminoAcidResultDTO
from nnaasynth.workflow_components.running import RunAiZynthFinder
from nnaasynth.workflow_components.scoring import FeasibilityScorer


class RunSynthesizabilityAnalysis:
    def __init__(self, chemistry: Protection, aizynthfinder_runner: RunAiZynthFinder, feasibility: FeasibilityScorer):
        self._chemistry = chemistry
        self._feasibility = feasibility
        self._aizynthfinder = aizynthfinder_runner

    def run_pipeline(self, amino_acid_smiles: str) -> List[AminoAcidResultDTO]:
        # Protect the amino acid
        protected_amino_acids = self._chemistry.protect_amino_acid(amino_acid_smiles)

        print("The number of protected versions for the input NNAA: ", len(protected_amino_acids))
        protected_amino_acids = protected_amino_acids[:2]

        # Run AizynthFinder
        outputs: List[AminoAcidDTO] = self._aizynthfinder.run_multiple_smiles(protected_amino_acids)

        protected_nnaas = []
        # Score the routes
        for nnaa_data in outputs:
            chemformer_scores, expert_augmented_scores = self.score_routes(nnaa_data.routes)
            nnaa_data.chemformer_scores = chemformer_scores
            nnaa_data.expert_augmented_scores = expert_augmented_scores

            # Select the best route
            selected_best_route = self.select_best_route(nnaa_data)
            protected_nnaas.append(selected_best_route)

        return protected_nnaas


    def select_best_route(self, nnaa_data: AminoAcidDTO) -> AminoAcidResultDTO:
        best_feasibility_score = min(nnaa_data.expert_augmented_scores)
        best_idx = nnaa_data.expert_augmented_scores.index(best_feasibility_score)
        amino_acid_results = AminoAcidResultDTO(smiles=nnaa_data.smiles,
                                                routes=nnaa_data.routes[best_idx],
                                                chemformer_score=nnaa_data.chemformer_scores[best_idx],
                                                expert_augmented_score=nnaa_data.expert_augmented_scores[best_idx],
                                                protection_groups=nnaa_data.protection_groups,
                                                )
        print(f"Protected Amino Acid: {nnaa_data.smiles}\nBest route has Chemformer score: {amino_acid_results.chemformer_score} and Expert Augmented score: {amino_acid_results.expert_augmented_score}\n")
        return amino_acid_results

    def score_routes(self, routes: List[SynthesisRoute]):
        chemformer_scores = [self._feasibility.score_with_chemformer(route) for route in routes]
        expert_augmented_scores = [self._feasibility.score_with_expert_augmented_feasibility(route, sc) for route, sc in zip(routes, chemformer_scores)]
        return chemformer_scores, expert_augmented_scores

