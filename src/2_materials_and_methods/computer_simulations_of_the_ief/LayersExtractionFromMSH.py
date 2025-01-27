"""
Description:
------------
Extracts specific layers (gray matter, white matter, and eye balls) from a brain mesh file (
'MNI152_TDCS_1_scalar.msh') using SimNIBS, and saves the result as
'extracted_magnE_gm_wm_eb.msh'.
"""

import os
import simnibs  # v 4.0.1

# Read the simulation result
head_mesh = simnibs.read_msh(
    os.path.join('simnibs/results', 'MNI152_TDCS_1_scalar.msh')
)

# Crop the mesh
msh = head_mesh.crop_mesh([1, 2, 6])  # 1: GM, 2: WM, 3: CSF, 5: Scalp, 6: Eye balls

msh.write('simnibs/results/extracted_gm_wm_eb.msh')
