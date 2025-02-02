import nibabel as nib
import numpy as np

field_type = 'magnE'  # Replace with 'magnE' or 'magnJ'
configuration = 'periorbital'  # Replace with 'periorbital' or 'frontal_occipital'

# Load the NIfTI files
magnE_img = nib.load(f"../../data/ief/{configuration}_conf_{field_type}.nii.gz")
rois_img = nib.load("../../data/ief/rois.nii.gz")

# Get data arrays
magnE_data = magnE_img.get_fdata()
rois_data = rois_img.get_fdata()
rois_data = np.squeeze(rois_data, axis=-1)  # Remove the last dimension

print(rois_data.shape)

# Get unique ROI labels (excluding background 0)
roi_labels = np.unique(rois_data)
roi_labels = roi_labels[roi_labels > 0]  # Exclude background

# Calculate mean magnitude electric field values for each ROI
roi_means = {}
for roi in roi_labels:
    roi_mask = rois_data == roi
    roi_means[roi] = np.mean(magnE_data[roi_mask])

# Define ROI labels
roi_labels_dict = {
    0: "Background",
    1: "Eyeballs",
    2: "Optic Nerves",
    4: "Rest of the Brain"
}

# Print the results with ROI labels
for roi, mean_value in roi_means.items():
    roi_label = roi_labels_dict.get(int(roi), "Unknown ROI")  # Get label, default to "Unknown ROI" if not found
    print(f"ROI {int(roi)} ({roi_label}): Mean Magnitude Electric Field = {mean_value:.6f} mV/mm")
