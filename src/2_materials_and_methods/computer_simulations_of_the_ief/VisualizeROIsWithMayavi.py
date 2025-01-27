"""
Description:
------------
This script visualizes regions of interest (ROIs) from a NIfTI file using the Mayavi library.
It loads the NIfTI file, swaps specific values within the data for visualization purposes, and
displays the 3D volume with an interactive colorbar.
"""

import nibabel as nib
from mayavi import mlab
import numpy as np

# Load the NIfTI file
nii_rois_file = 'rois_eyeballs_opticnerves_restofthebrain.nii.gz'
img = nib.load(nii_rois_file)
data = img.get_fdata()

# Swap values 3 and 1
swapped_data = np.where(data == 4, 1, np.where(data == 1, 4, data))

# Ensure data is 3D
if swapped_data.ndim == 4:
    swapped_data = swapped_data[..., 0]  # Take the first volume if there are multiple volumes

# Display
mlab.figure()
src = mlab.pipeline.scalar_field(swapped_data)
vol = mlab.pipeline.volume(src, vmin=swapped_data.min(), vmax=swapped_data.max())

mlab.colorbar()
mlab.show()
