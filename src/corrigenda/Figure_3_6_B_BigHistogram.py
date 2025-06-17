"""
EFM (mesh) maximum values (V/m) read from SimNIBS for Periorbital configuration:

Old maximum (ellipse 3 cm²):      1.7609

Rectangle 3 cm² (front):          1.78761
Elliptical 3 cm² (front):         1.76803
Elliptical (no 3 cm²) (front):    1.89053

New maximum (elliptical 3 cm²):    1.76803
"""

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

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

# Load and calculate distributions for two images
image_path1 = 'data/ief/electrodes/cropped_periorbital_eliptical_no3cm2.png'
image_path2 = 'data/ief/electrodes/cropped_periorbital_rectangular_3cm2.png'
unique_values1, percentages1 = get_distribution(image_path1)
unique_values2, percentages2 = get_distribution(image_path2)

# Plot the distributions of pixel values for both images
plt.figure(figsize=(5, 3)) # plt.figure(figsize=(5, 3))
plt.bar(unique_values1, percentages1, width=0.02, alpha=0.5, label='Elipsoid', color='red', edgecolor='black')
plt.bar(unique_values2, percentages2, width=0.02, alpha=0.5, label='Rectangle', color='blue', edgecolor='black')

# Font size
fs = 12

# Increase font sizes
plt.xlabel('Normalized Electric Field Magnitude (V/m)', fontsize=fs)
plt.ylabel('Percentage of Values (%)', fontsize=fs)
plt.xticks(fontsize=fs)
plt.yticks(fontsize=fs)
plt.legend(fontsize=fs)
plt.ylim(0, 3)
plt.xlim(0, 1.05)

plt.tight_layout()
plt.savefig('Corrigenda Figure 3-6B BigHistagram.png', dpi=300, bbox_inches='tight', transparent=True)
# plt.show()
