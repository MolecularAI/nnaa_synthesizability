from typing import List, Dict, Tuple

from pydantic.dataclasses import dataclass


@dataclass
class AminoAcidDTO:
    smiles: str
    routes: List
    stats: Dict
    chemformer_scores: List[float] = None
    expert_augmented_scores: List[float] = None
    protection_groups: Tuple[str, ...] = None


