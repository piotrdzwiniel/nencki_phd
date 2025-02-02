import matplotlib.pyplot as plt
import numpy as np

# Data
regions = ['Eyeballs', 'Optic Nerve', 'Rest of the Brain']
means = [0.01268, -0.01062, -0.00237]
sds = [0.0112, 0.00881, 0.00092]
mins = [-0.02364, -0.03783, -0.02461]
maxs = [0.04835, -0.00052, 0.00223]

# Plot
plt.figure(figsize=(5.5, 5))
bar_width = 0.75
colors = ['gray', 'gray', 'gray']  # More professional color palette

bars = plt.bar(regions, means, yerr=sds, capsize=5, color=colors, alpha=0.8, edgecolor='black', width=bar_width)
plt.axhline(0, color='gray', linewidth=1.0, alpha=0.6)

# Fixed position for annotations
fixed_y_position = 0.03  # Fixed vertical location for all annotations

# Add annotations at the fixed y position
iterator = 0
for bar, mean, min_val, max_val in zip(bars, means, mins, maxs):
    x_pos = bar.get_x() + bar.get_width() / 2
    if iterator != 1:
        fixed_y_position = -fixed_y_position
    else:
        fixed_y_position = 0.03
    plt.text(x_pos, fixed_y_position,
             f'Mean: {mean:.3f}\nMin: {min_val:.3f}\nMax: {max_val:.3f}',
             ha='center', va='center', fontsize=12, bbox=dict(facecolor='white', alpha=0.5))
    iterator += 1

# Labels and title
plt.ylabel('Mean Difference', fontsize=15)
# plt.title('Mean Difference in Brain Regions (Facial - Occipital)', fontsize=16)
plt.xticks(fontsize=15, rotation=45)
plt.yticks(fontsize=15)
plt.ylim(-0.06, 0.06)  # Adjusting y-limits for better visibility of fixed annotations
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
# plt.savefig('difference_ROIS.png', dpi=300, bbox_inches='tight', transparent=True)
plt.show()
