from PIL import Image
import numpy as np

def get_distribution(image_path):
    # Load the image and convert to grayscale
    image = Image.open(image_path).convert('L')
    # Convert image to a NumPy array and normalize values to range [0, 1]
    image_array = np.array(image) / 255.0
    # Calculate the distribution of values
    unique_values, counts = np.unique(image_array, return_counts=True)
    # Calculate percentages
    percentages = (counts / counts.sum()) * 100
    return unique_values, percentages

def get_percentage_in_range(unique_values, percentages, min_val=0.5, max_val=1.0):
    # Filter the values in the specified range
    in_range_mask = (unique_values >= min_val) & (unique_values <= max_val)
    percentage_in_range = percentages[in_range_mask].sum()
    return percentage_in_range

# Load and calculate distributions for two images
image_path1 = 'data/ief/electrodes/cropped_front_occip_ellipitcal_35cm2_rear_blacknwhite.png'
image_path2 = 'data/ief/electrodes/cropped_front_occip_rectangular_35cm2_rear_blacknwhite.png'
unique_values1, percentages1 = get_distribution(image_path1)
unique_values2, percentages2 = get_distribution(image_path2)

# Calculate percentages for values between 0.6 and 1.0 for each image
percentage_in_range1 = get_percentage_in_range(unique_values1, percentages1)
percentage_in_range2 = get_percentage_in_range(unique_values2, percentages2)

print(f"Percentage of values between 0.6 and 1.0 for Elipsoid: {percentage_in_range1:.2f}%")
print(f"Percentage of values between 0.6 and 1.0 for Rectangle: {percentage_in_range2:.2f}%")

# Dane dla wykresu słupkowego
categories = ['Elipsoid', 'Rectangle']
percentages = [percentage_in_range1, percentage_in_range2]

import matplotlib.pyplot as plt

# Wykres
# Increase font size of whole plot
plt.rcParams.update({'font.size': 12})
plt.figure(figsize=(1.5, 1.6))
plt.bar(categories, percentages, color=['red', 'blue'], alpha=0.7, edgecolor='black')
plt.ylabel('%')
# plt.title('Percentage of Values Between 0.6 and 1.0')
plt.ylim(0, 5.5)  # Dopasowanie limitu osi Y dla lepszej wizualizacji
# Create yticks from 0 to 5, but with step of 2.5
plt.yticks([0, 1, 2, 3, 4, 5])
plt.xticks([])
plt.tight_layout()

# plt.savefig('Corrigenda Figure 3-9B Percentages.png', dpi=300, bbox_inches='tight', transparent=True)
plt.show()
