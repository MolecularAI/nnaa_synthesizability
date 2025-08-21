# Non-Natural Amino Acid Synthesizability Analysis

This repository provides an end-to-end framework for analyzing the synthetic accessibility of non-natural amino acids (NNAAs) and their protected forms. It leverages cheminformatics tools and deep learning models to:
- Generate protected forms of input amino acids
- Perform retrosynthetic analysis using AiZynthFinder
- Score synthetic routes using Chemformer and expert-augmented feasibility models
- Select the best synthetic route for each protected form

The workflow is designed to support peptide and amino acid design projects exploring beyond the standard 20 natural amino acids.

## Features 
- **Automated protection** of amino acids using customizable protection group rules
- **Retrosynthetic analysis** via AiZynthFinder
- **Feasibility scoring** using Chemformer and expert-augmented models
- **Extensible and modular** end-to-end pipeline for synthesizability analysis

## Required External Repositories and Model Files

Before using this repository, you must manually install the following external tools and libraries from their respective GitHub repositories:

- **AiZynthFinder**  
  Retrosynthetic planning software and its environment to run this project.
  GitHub: https://github.com/MolecularAI/aizynthfinder


- **reaction-utils**  
  Repo for reaction data handling and cheminformatics utilities.  
  GitHub: https://github.com/MolecularAI/reaction_utils


- **AiZynthModels**  
  Provides models and environment for AiZynthFinder and Chemformer API.   
  GitHub: https://github.com/MolecularAI/aizynthmodels


- **Chemformer**  
  Transformer-based model for reaction and molecule prediction. **You will need to obtain only the vocabulary to run Chemformer API (bart_vocab_downstream.json)**
  GitHub: https://github.com/chemprop/chemformer  
  

- **Expert-Augmented Scorer Model Files**
To use the expert-augmented scoring models, download the following files into a folder named `expert_augmented_models`:
  ```bash
  mkdir expert_augmented_models
  cd expert_augmented_models
  wget https://zenodo.org/records/14533779/files/deepset_route_scoring_sdf.onnx?download=1 -O deepset_route_scoring_sdf.onnx
  wget https://zenodo.org/records/14533779/files/reaction_class_ranks.csv?download=1 -O reaction_class_ranks.csv
  wget https://zenodo.org/records/14533779/files/scscore_model_1024_bits.onnx?download=1 -O scscore_model_1024_bits.onnx
  wget https://raw.githubusercontent.com/MolecularAI/reaction_utils/refs/heads/route-scoring-example/examples/route-scoring/example-routes.json
   ```
## Installation
1. Clone this repository
2. Create the environment from AiZynthFinder and AiZynthModels:
   - The `aizynthfinder` repository provides the environment to run this pipeline.
   - The `aizynthmodels` repository provides the environment to run the Chemformer API.
   
3. Install reaction-utils dependencies to both environments:
```bash
  cd ../reaction_utils
  poetry install --all-extras
  ```
   
4. Prepare the following resources (also described in the `example.ipynb`):
   - AiZynthFinder configuration file (example in `nnaasynth/aizynthfinder_setup/aizynth_config.yml`)
     - Download the public model and stock files as described in the AiZynthFinder repository. 
   - Protection group and reaction rules CSVs (stored in `reaction-utils/examples/nnaa/`)
   - DeepSet and SCScore model files (described above)

5. Run the Chemformer API 
Chemformer API can be run locally with the bash script and the model checkpoint provided in the `nnaasynth/chemformer_api` folder. 
To run the API, you need to:
- set the required paths in chemformer_api.sh
- run the api and obtain the port number
```bash
   conda activate aizynthmodels
   bash chemformer_api.sh
   ```
- In case of a different model, please ensure it is compatible with the Chemformer API.

## Project Structure
- **`example.ipynb`** — Jupyter notebook demonstrating usage
- **`run_synthesizability_analysis.py`** — Main pipeline class
- **`nnaasynth/`** — Main package directory
  - **`aizynthfinder_setup/`** — AiZynthFinder configuration and stock files
  - **`chemformer_api/`** — Chemformer API-related code (if any)
  - **`dtos/`** — Data transfer objects for amino acids and results
  - **`utils/`** — Utility functions
  - **`workflow_components/`** — Core modules for protection, scoring, and running retrosynthesis

## Citation
If you use this codebase in your research, please cite the relevant tools (AiZynthFinder, Chemformer, reaction-utils) and our preprint:
```bibtex
@misc{geylan2025nnaasynth,
      title={From Concept to Chemistry: Integrating protection group strategy and reaction feasibility into non-natural amino acid synthesis planning}, 
      author={Gökçe Geylan and Mikhail Kabeshov and Samuel Genheden and Christos Kannas and Thierry Kogej and Leonardo De Maria and Florian David and Ola Engkvist},
      year={2025},
      eprint={10.26434/chemrxiv-2025-jtwn1},
      archivePrefix={ChemRxiv},
      url={https://chemrxiv.org/engage/chemrxiv/article-details/68592f151a8f9bdab5199312}, 
}
```

## License
This project is licensed under the Apache 2.0 License. See the `LICENSE` file for more details.

## Contact
For questions or contributions, please contact Gökçe Geylan at gokcegeylan96@gmail.com
