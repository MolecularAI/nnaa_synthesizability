from typing import Any, Tuple

from pydantic.dataclasses import dataclass
from rxnutils.routes.base import SynthesisRoute


@dataclass
class AminoAcidResultDTO:
    smiles: str
    routes: Any #SynthesisRoute
    chemformer_score: float
    expert_augmented_score: float
    protection_groups: Tuple[str, ...] = None


