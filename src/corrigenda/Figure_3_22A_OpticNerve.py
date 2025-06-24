import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

ROI = {
    'Eyeballs': ['Eyeballs', 1],
    'Optic Nerve': ['Optic Nerve', 2],
    'Rest Of The Brain': ['Rest of the Brain', 3]
}
chosen_roi = 'Optic Nerve'
roi_label = ROI[chosen_roi][0]
roi_value = ROI[chosen_roi][1]

# Load ROI data
roi_nii_file = 'data/ief/eb_on_rotb_roi.nii.gz'
img_roi = nib.load(roi_nii_file)
data_roi = img_roi.get_fdata()
data_roi = np.squeeze(data_roi)
data_roi[data_roi == 4] = 3

"""
Description of the value in data_roi:

0: Background
1: Eyeballs
2: Optic Nerve
3: Rest of the Brain (GM, WM)
"""

# Load nii.gz file for Condition 1
condition1_nii_file = 'data/ief/periorbital/cec_gm_wm_eb_magnE.nii.gz'
# Replace with your file path
img_cond1 = nib.load(condition1_nii_file)
data_cond1 = img_cond1.get_fdata()

# Load nii.gz file for Condition 2
condition2_nii_file = ('data/ief/frontal_occipital/cec_gm_wm_eb_magnE.nii.gz')
img_cond2 = nib.load(condition2_nii_file)
data_cond2 = img_cond2.get_fdata()

# Extract values only for Eyeballs based on data_roi (value 1)
mask = (data_roi == roi_value)
values_cond1 = data_cond1[mask]
values_cond2 = data_cond2[mask]

values_cond1 = np.array(values_cond1).flatten()
values_cond2 = np.array(values_cond2).flatten()

# Find the total minimum and maximum across both datasets
total_min = min(values_cond1.min(), values_cond2.min())
total_max = max(values_cond1.max(), values_cond2.max())

# Normalize the values using the global minimum and maximum
values_cond1 = (values_cond1 - total_min) / (total_max - total_min)
values_cond2 = (values_cond2 - total_min) / (total_max - total_min)

weights1 = np.ones_like(values_cond1) / len(values_cond1)
weights2 = np.ones_like(values_cond2) / len(values_cond2)

import pandas as pd

df1 = pd.DataFrame({'data': values_cond1, 'weights': weights1})
df2 = pd.DataFrame({'data': values_cond2, 'weights': weights2})

from scipy.stats import ks_2samp

"""
Kolmogorov-Smirnov (KS) Test
Purpose: Compares the entire distribution functions of two datasets.
When to Use: If you want to assess whether the two distributions are significantly different in terms of their shapes (not limited to their central tendencies).
Limitations: More sensitive to differences in the central part of the distribution than at the tails.
"""

stat, p_value = ks_2samp(values_cond1, values_cond2)
print(f"KS Test Statistic: {stat:.4f}, p-value: {p_value:.4f}")

# Compact and aesthetically pleasing visualization
# colors = ['#FF2600', '#4181FF']
colors = ['dimgray', 'darkorange']
plt.figure(figsize=(3, 3), dpi=150)  # Small, high-resolution figure

sns.kdeplot(data=df2, x='data', color=colors[0], alpha=0.75, label='Frontal-Occipital', linewidth=2, cumulative=True, weights='weights')
sns.kdeplot(data=df1, x='data', color=colors[1], alpha=0.75, label='Periorbital', linewidth=2, cumulative=True, weights='weights')

plt.title(f'Distribution\nfor {chosen_roi} ROI')
plt.ylabel('Cumulative Density')

# Convert y-axis values to percentages
ax = plt.gca()  # Get the current axis
y_ticks = ax.get_yticks()  # Get current y-tick values
ax.set_yticklabels([f'{100 * val:.0f}%' for val in y_ticks])  # Format y-tick values as percentages

plt.xlabel('EFM (V/m)')

plt.xlim(0, 1)
plt.xticks([0.0, 0.5, 1.0])
plt.ylim(0, 1.1)

plt.tight_layout()
plt.legend(frameon=False, loc='lower right')
# plt.savefig(f'Corrigenda Figure 3-22A_{chosen_roi.replace(" ", "")}_EFM.png', dpi=300, bbox_inches='tight', transparent=True)
plt.show()
