from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import ks_2samp
import seaborn as sns

def get_values(image_path):
    # Load the image and convert to grayscale
    image = Image.open(image_path).convert('L')
    # Convert image to a NumPy array and normalize values to range [0, 1]
    image_array = np.array(image) / 255.0
    return image_array.flatten()

image_path1 = 'data/ief/electrodes/cropped_front_occip_ellipitcal_35cm2_rear_blacknwhite.png'
image_path2 = 'data/ief/electrodes/cropped_front_occip_rectangular_35cm2_rear_blacknwhite.png'

values_cond1 = get_values(image_path1)
values_cond2 = get_values(image_path2)

# Downsample the data
values_cond1 = values_cond1[::100]
values_cond2 = values_cond2[::100]

# Find the total minimum and maximum across both datasets
total_min = min(values_cond1.min(), values_cond2.min())
total_max = max(values_cond1.max(), values_cond2.max())

# Normalize the values using the global minimum and maximum
values_cond1 = (values_cond1 - total_min) / (total_max - total_min)
values_cond2 = (values_cond2 - total_min) / (total_max - total_min)

weights1 = np.ones_like(values_cond1) / len(values_cond1)
weights2 = np.ones_like(values_cond2) / len(values_cond2)

df1 = pd.DataFrame({'data': values_cond1, 'weights': weights1})
df2 = pd.DataFrame({'data': values_cond2, 'weights': weights2})

"""
Kolmogorov-Smirnov (KS) Test
Purpose: Compares the entire distribution functions of two datasets.
When to Use: If you want to assess whether the two distributions are significantly different in terms of their shapes (not limited to their central tendencies).
Limitations: More sensitive to differences in the central part of the distribution than at the tails.
"""

# Choosse values only between 0.6 and 1.0
values_cond1 = values_cond1[(values_cond1 >= 0.4) & (values_cond1 <= 1.0)]
values_cond2 = values_cond2[(values_cond2 >= 0.4) & (values_cond2 <= 1.0)]

stat, p_value = ks_2samp(values_cond1, values_cond2)
print(f"KS Test Statistic: {stat:.3f}, p-value: {p_value:.4f}")

# Compact and aesthetically pleasing visualization
colors = ['red', 'blue']

plt.rcParams.update({'font.size': 11})
plt.figure(figsize=(4, 4), dpi=150)  # Small, high-resolution figure

sns.kdeplot(data=df2, x='data', color=colors[1], alpha=0.75, label='Rectangle', linewidth=2, cumulative=True, weights='weights')
sns.kdeplot(data=df1, x='data', color=colors[0], alpha=0.75, label='Elipsoid', linewidth=2, cumulative=True, weights='weights')

plt.title(f'Cumulative Densities', pad=20, fontsize=12)
plt.ylabel('Cumulative Density')

# Convert y-axis values to percentages
ax = plt.gca()  # Get the current axis
y_ticks = ax.get_yticks()  # Get current y-tick values
ax.set_yticklabels([f'{100 * val:.0f}%' for val in y_ticks])  # Format y-tick values as percentages

plt.xlabel('Normalized EFM (V/m)')

plt.xlim(0, 1)
plt.xticks([0.0, 0.5, 1.0])
plt.ylim(0, 1.1)

plt.tight_layout()
plt.legend(frameon=False, loc='lower right')
# plt.savefig('Corrigenda Figure 3-9C Difference.png', dpi=300, bbox_inches='tight', transparent=True)
plt.show()
