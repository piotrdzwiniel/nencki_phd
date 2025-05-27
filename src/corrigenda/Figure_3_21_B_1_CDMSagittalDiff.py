import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FuncFormatter

# Load the first NIfTI file (T1)
file_path_1 = 'data/ief/T1.nii.gz'  # Replace with your file path
img1 = nib.load(file_path_1)
data1 = img1.get_fdata()

# Get the center index in the X (sagittal) dimension for the first data
center_x1 = data1.shape[0] // 2
sagittal_slice1 = np.mean(data1[75:76, :, :], axis=0)  # Extract the sagittal slice at the center

print(f"Center slice: {center_x1}")

# Load the second NIfTI file (stacked data)
file_path_2 = 'data/ief/periorbital/cec_gm_wm_eb_magnJ.nii.gz' # Replace with your file path
img2 = nib.load(file_path_2)
data2 = img2.get_fdata()

print(f"Shape of second data: {data2.shape}")

# Get the center index and range for stacking slices in the second data
center_x2 = data2.shape[0] // 2
slice_range = 30  # Number of slices to include on each side of the center
start_idx = 44 # 109 # max(center_x2 - slice_range, 0)
end_idx = 75 # 135 # min(center_x2 + slice_range, data2.shape[0])
stacked_slices_facial = np.mean(data2[start_idx:end_idx, :, :], axis=0)  # Averaging for stacking

# Mask zero values in the stacked slices
stacked_slices_facial[stacked_slices_facial == 0] = np.nan  # Set zero values to NaN for transparency

# Load the second NIfTI file (stacked data)
file_path_3 = 'data/ief/frontal_occipital/cec_gm_wm_eb_magnJ.nii.gz'  # Replace with your file path
img3 = nib.load(file_path_3)
data3 = img3.get_fdata()

print(f"Shape of third data: {data3.shape}")

# Get the center index and range for stacking slices in the second data
center_x3 = data3.shape[0] // 2
slice_range = 30  # Number of slices to include on each side of the center
start_idx = 44 # 109 # max(center_x2 - slice_range, 0)
end_idx = 75 # 135 # min(center_x2 + slice_range, data2.shape[0])
stacked_slices_occipital = np.mean(data3[start_idx:end_idx, :, :], axis=0)  # Averaging for stacking

# Mask zero values in the stacked slices
stacked_slices_occipital[stacked_slices_occipital == 0] = np.nan  # Set zero values to NaN for transparency

stacked_slices = stacked_slices_facial - stacked_slices_occipital

# Plotting the combined view
plt.figure(figsize=(8, 5))

# Display the base sagittal slice (first data)
plt.imshow(sagittal_slice1.T, cmap='gray', origin='lower')  # Transpose for correct orientation

# Curve slope
slope = 6.5

# Generate values for replication
x = np.linspace(0, 0.5, 100)
y = 1 - np.exp(-slope * x)
y = np.flip(y, axis=0)

x2 = np.linspace(0.5, 1.0, 100)
y2 = 1 - np.exp(-slope * x)

alpha_1 = [(x, y, y) for x, y in zip(x, y)]

alpha_2 = [(x2, y2, y2) for x2, y2 in zip(x2, y2)]

# Remove first element from alpha_2
alpha_2.pop(0)

# Concatenate the lists
alpha = alpha_1 + alpha_2

# Create a custom colormap with blue -> transparent -> red transition
cdict = {
    'red':   [(0.0, 0.0, 0.0),   # Blue
              (0.5, 1.0, 1.0),   # Middle (transparent point in terms of RGB intensity)
              (1.0, 1.0, 1.0)],  # Red
    'green': [(0.0, 0.0, 0.0),   # Blue
              (0.5, 1.0, 1.0),   # Middle (transparent point in terms of RGB intensity)
              (1.0, 0.0, 0.0)],  # Red
    'blue':  [(0.0, 1.0, 1.0),   # Blue
              (0.5, 1.0, 1.0),   # Middle (transparent point in terms of RGB intensity)
              (1.0, 0.0, 0.0)],  # Red
    'alpha': alpha
}

# Create a colormap
blue_to_transparent_to_red = LinearSegmentedColormap('BlueTransparentRed', cdict)

# Overlay the stacked slices (second data) with transparency
plt.imshow(stacked_slices.T, cmap=blue_to_transparent_to_red, origin='lower', interpolation='nearest', vmin=-0.025, vmax=0.025)  # Adjust alpha for transparency

# Font size
fs = 16

# Add title and labels with increased font size
plt.xlabel('Y-axis (mm)', fontsize=fs)
plt.ylabel('Z-axis (mm)', fontsize=fs)
plt.xticks(fontsize=fs)
plt.yticks(fontsize=fs)
plt.ylim(100)

# Create colorbar
cbar = plt.colorbar(location='left', fraction=0.025, pad=0.15)
cbar.ax.tick_params(labelsize=fs)
cbar.set_label('CDM (A/m2)', fontsize=fs)

# Format colorbar ticks without leading zero
formatter = FuncFormatter(lambda x, _: f'{x:.3f}'.replace("0.", ".") if x != 0 else "0")
cbar.ax.yaxis.set_major_formatter(formatter)

# Layout and save
plt.tight_layout()
plt.savefig('Corrigenda Figure 3-21B1.png', dpi=300, bbox_inches='tight', transparent=True)
# plt.show()