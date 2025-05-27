import nibabel as nib

# Type of the field
field_type = "magnJ"

# Load the first NIfTI file (facial data)
file_path_2 = f'data/ief/periorbital/cec_gm_wm_eb_{field_type}.nii.gz'  # Replace with your file path
img2 = nib.load(file_path_2)
data2 = img2.get_fdata()

# Load the second NIfTI file (occipital data)
file_path_3 = f'data/ief/frontal_occipital/cec_gm_wm_eb_{field_type}.nii.gz'  # Replace with your file path
img3 = nib.load(file_path_3)
data3 = img3.get_fdata()

# Ensure both datasets have the same shape
if data2.shape != data3.shape:
    raise ValueError("The input NIfTI files must have the same shape.")

# Subtract the occipital data from the facial data
difference_data = data2 - data3

# Create a new NIfTI image for the difference data
difference_img = nib.Nifti1Image(difference_data, affine=img2.affine, header=img2.header)

# Save the resulting difference as a new NIfTI file
output_path = f'data/ief/cec_gm_wm_eb_{field_type}_between_conf_diff.nii.gz'  # Replace with your desired output path
nib.save(difference_img, output_path)

print(f"Difference NIfTI file saved at: {output_path}")
