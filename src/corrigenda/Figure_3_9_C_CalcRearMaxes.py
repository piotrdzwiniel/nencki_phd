from PIL import Image
import numpy as np


def get_values(image_path):
    # Load the image and convert to grayscale
    image = Image.open(image_path).convert('L')
    # Convert image to a NumPy array and normalize values to range [0, 1]
    image_array = np.array(image) / 255.0
    return image_array.flatten()

image_path1 = 'data/ief/electrodes/cropped_front_occip_elliptical_35cm2_rear_blacknwhite_recmax.png'
image_path2 = 'data/ief/electrodes/cropped_front_occip_rectangular_35cm2_rear_blacknwhite_recmax.png'

values_cond1 = get_values(image_path1)
values_cond2 = get_values(image_path2)

# Downsample the data
values_cond1 = values_cond1[::100]
values_cond2 = values_cond2[::100]

current_max = 1.0
new_max_e = 1.57148
new_max_r = 1.62229

# Compute scaling factor and renormalize
scaling_factor_e = new_max_e / current_max
scaling_factor_r = new_max_r / current_max

values_cond1 = values_cond1 * scaling_factor_e
values_cond2 = values_cond2 * scaling_factor_r

print(f'Elipsoid: {max(values_cond1):.3f}')
print(f'Rectangle: {max(values_cond2):.3f}')
