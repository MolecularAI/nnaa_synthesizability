import os
from typing import List

import matplotlib.pyplot as plt
from rdkit import Chem
from rdkit.Chem import Draw
import matplotlib.gridspec as gridspec

from nnaasynth.dtos.result_dto import AminoAcidResultDTO


def plot_results(query_smiles: str, outcomes: List[AminoAcidResultDTO], save_path: str = None):
    fig = plt.figure(figsize=(20, 16))
    n = len(outcomes)

    gs = gridspec.GridSpec(n + 1, 12)
    gs.update(wspace=0.5)

    ax_img = fig.add_subplot(gs[0, 2:4])
    mol2 = Chem.MolFromSmiles(query_smiles)
    img2 = Draw.MolToImage(mol2, size=(400, 400))
    ax_img.imshow(img2, interpolation="catrom", aspect="auto")
    ax_img.set_title("Query Non-Natural Amino Acid", fontsize=10)
    ax_img.get_xaxis().set_visible(False)
    ax_img.get_yaxis().set_visible(False)

    for i, out in enumerate(outcomes):
        ax1 = fig.add_subplot(gs[i + 1, :2])
        mol = Chem.MolFromSmiles(out.smiles)
        im1 = Draw.MolToImage(mol, size=(400, 400))
        ax1.imshow(im1, interpolation="catrom", aspect="auto")
        ax1.get_xaxis().set_visible(False)
        ax1.get_yaxis().set_visible(False)

        ax2 = fig.add_subplot(gs[i + 1, 2:4])
        table = ax2.table(cellText=[
            ["Protection\nstrategy", f"{out.protection_groups}"],
            ["Chemformer\nscore", f"{out.chemformer_score:.2}"],
            ["Expert-Augmented\nscore", f"{out.expert_augmented_score:.2}"]
        ],
            bbox=(0, 0, 1, 1),
            cellLoc="center")
        table.set_fontsize(25)
        ax2.get_xaxis().set_visible(False)
        ax2.get_yaxis().set_visible(False)

        ax3 = fig.add_subplot(gs[i + 1, 4:])
        im2 = out.routes.image()
        ax3.imshow(im2, interpolation="catrom", aspect="auto")
        ax3.get_xaxis().set_visible(False)
        ax3.get_yaxis().set_visible(False)
    plt.show()
    fig.savefig(os.path.join(save_path), bbox_inches='tight', dpi=400)