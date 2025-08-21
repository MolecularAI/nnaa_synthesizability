from typing import List

from rxnutils.chem.protection.amino_acids import preprocess_amino_acids, AminoAcidProtectionEngine


class Protection:
    def __init__(self, smartslib_path=None, reaction_rules_path=None, protection_groups_path=None):
        """
        Initialize Chemistry utility class for handling chemical structures and amino acid protection.

        Parameters:
        -----------
        smartslib_path: str, optional
            Path to the SMARTS library file for reactive functions
        reaction_rules_path: str, optional
            Path to the reaction rules CSV file
        protection_groups_path: str, optional
            Path to the protection groups CSV file
        """
        self.engine = None
        if all([smartslib_path, reaction_rules_path, protection_groups_path]):
            self._setup_protection_engine(smartslib_path, reaction_rules_path, protection_groups_path)
        else:
            raise ValueError("smartslib_path, reaction_rules_path and protection_groups_path must be provided")

    def _setup_protection_engine(self, smartslib_path, reaction_rules_path, protection_groups_path):
        self.engine = AminoAcidProtectionEngine(
            smartslib_path=smartslib_path,
            reaction_rules_path=reaction_rules_path,
            protection_groups_path=protection_groups_path
        )

    def protect_amino_acid(self, smiles: str) -> List:
        if self.engine is None:
            raise ValueError("Protection engine not set up. Call setup_protection_engine first.")

        # Preprocess amino acid to handle charged species
        uncharged_smiles = preprocess_amino_acids(smiles)

        # Protect the amino acid
        protected_amino_acids = self.engine(uncharged_smiles)
        return protected_amino_acids
