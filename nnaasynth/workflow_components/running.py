import time
from typing import List, Dict

import yaml
from aizynthfinder.aizynthfinder import AiZynthFinder
from rxnutils.chem.protection.amino_acids import ProtectedAminoAcid
from rxnutils.routes.base import SynthesisRoute

from nnaasynth.dtos.aminoacid_dto import AminoAcidDTO


class RunAiZynthFinder:
    def __init__(self, config_path: str):
        self._config_path = config_path
        self.finder = self._initialize_finder(self._config_path)

    def _initialize_finder(self, config_path) -> AiZynthFinder:
        finder = AiZynthFinder(configfile=config_path)

        with open(self._config_path, 'r') as f:
            self._config = yaml.safe_load(f)

        stocks = list(self._config["stock"].keys())
        finder.stock.select(stocks)

        expansion = list(self._config["expansion"].keys())
        finder.expansion_policy.select(expansion)

        filter_policy = list(self._config["filter"].keys())
        finder.filter_policy.select(filter_policy)
        return finder

    def run_single_smiles(self, protected_amino_acid: ProtectedAminoAcid) -> AminoAcidDTO:
        target_smiles = protected_amino_acid.smiles
        protection_groups = protected_amino_acid.protection_groups
        try:
            self.finder.target_smiles = target_smiles
            self.finder.tree_search()
            self.finder.build_routes()

            routes = [SynthesisRoute(dict_) for dict_ in self.finder.routes.dicts]
            result = AminoAcidDTO(smiles=target_smiles,
                                  routes=routes,
                                  stats=self.get_statistics(),
                                  protection_groups=protection_groups,
                                  )

        except Exception as e:
            print(f"Error processing {target_smiles}: {str(e)}")
            result = AminoAcidDTO(smiles=target_smiles,
                                  routes=[],
                                  stats={},
                                  protection_groups=protection_groups,
                                  )
        return result

    def run_multiple_smiles(self, smiles_list: List[ProtectedAminoAcid]) -> List[AminoAcidDTO]:
        results = []
        total = len(smiles_list)

        print(f"Running AiZynthFinder on {total} SMILES")
        start_time = time.time()

        for i, protected_aa in enumerate(smiles_list):
            result = self.run_single_smiles(protected_aa)
            results.append(result)
            progress = i / total * 100
            routes_found = len(result.routes)
            print(f"[{progress:.1f}%] {i}/{total} - Processed {result.smiles}: {routes_found} routes found")

        total_time = time.time() - start_time
        print(f"Completed processing {total} SMILES in {total_time:.1f} seconds\n\n")

        return results

    def get_statistics(self) -> Dict:
        stats = self.finder.extract_statistics()
        return stats

    def get_route_image(self, route_id):
        return self.finder.routes.images[route_id]

    @staticmethod
    def convert_routes(aizynthfinder_output: AiZynthFinder) -> List[SynthesisRoute]:
        routes = aizynthfinder_output.routes.dicts
        extracted_routes = [SynthesisRoute(dict_) for dict_ in routes]
        return extracted_routes
