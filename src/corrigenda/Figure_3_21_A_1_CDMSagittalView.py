import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np

# Load the first NIfTI file (T1)
file_path_1 = 'data/ief/T1.nii.gz'  # Replace with your file path
img1 = nib.load(file_path_1)
data1 = img1.get_fdata()

# Get the center index in the X (sagittal) dimension for the first data
center_x1 = data1.shape[0] // 2
sagittal_slice1 = np.mean(data1[75:76], axis=0)  # Extract the sagittal slice at the center

# Voxel index for the slice (x-coordinate in voxel space)
voxel_index = np.array([75, 0, 0, 1])  # [x, y, z, 1] in homogeneous coordinates

affine = img1.affine

# Convert voxel index to MNI coordinate using the affine matrix
mni_coord = np.dot(affine, voxel_index)

# Output the MNI coordinate
print(f"MNI coordinate of the sagittal slice: {mni_coord[0]:.2f}, {mni_coord[1]:.2f}, {mni_coord[2]:.2f}")

print(f"Center slice: {center_x1}")

# Load the second NIfTI file (stacked data)
file_path_2 = 'data/ief/periorbital/cec_gm_wm_eb_magnJ.nii.gz'  # Replace with your file path
img2 = nib.load(file_path_2)
data2 = img2.get_fdata()

print(f"Shape of second data: {data2.shape}")

# Get the center index and range for stacking slices in the second data
center_x2 = data2.shape[0] // 2
slice_range = 30  # Number of slices to include on each side of the center
start_idx = 44
end_idx = 75
stacked_slices = np.mean(data2[start_idx:end_idx, :, :], axis=0)  # Averaging for stacking

# Mask zero values in the stacked slices
stacked_slices[stacked_slices == 0] = np.nan  # Set zero values to NaN for transparency

# Plotting the combined view
plt.figure(figsize=(8, 5))

# Display the base sagittal slice (first data)
plt.imshow(sagittal_slice1.T, cmap='gray', origin='lower')  # Transpose for correct orientation

# Overlay the stacked slices (second data) with transparency
plt.imshow(stacked_slices.T, cmap='jet', origin='lower', alpha=0.5, interpolation='nearest', vmin=0, vmax=0.05)  # Adjust alpha for transparency

# Font size
fs = 14

# Add title and labels with increased font size
plt.xlabel('Y-axis (mm)', fontsize=fs)
plt.ylabel('Z-axis (mm)', fontsize=fs)
plt.xticks(fontsize=fs)
plt.yticks(fontsize=fs)
plt.ylim(100)
cbar = plt.colorbar(location='left', fraction=0.025, pad=0.125)
cbar.ax.tick_params(labelsize=fs)  # Increase font size for colorbar ticks
cbar.set_label('CDM (A/m2)', fontsize=fs)  # Increase font size for colorbar label
plt.tight_layout()

# Save the figure
# plt.savefig('Corrigenda Figure 3-21A1.png', dpi=300, bbox_inches='tight', transparent=True)
plt.show()
