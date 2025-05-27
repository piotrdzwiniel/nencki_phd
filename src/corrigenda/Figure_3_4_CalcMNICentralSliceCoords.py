import nibabel as nib
import numpy as np

img = nib.load("data/ief/T1.nii.gz")
affine = img.affine
voxel_index = np.array([75, 0, 0, 1])
mni_coord = np.dot(affine, voxel_index)

print(mni_coord[:3])  # x, y, z w przestrzeni MNI