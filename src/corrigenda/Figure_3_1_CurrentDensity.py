import numpy as np
import matplotlib.pyplot as plt

# Define the range for current amplitude (0 to 0.5 mA) and area (0.1 to 5 cm²)
current_amplitude = np.linspace(0.01, 0.5, 100)  # Avoid zero to prevent division by zero
area = np.linspace(0.1, 5, 100)  # Start from a small area to avoid zero division

# Create a meshgrid for the X and Y values
X, Y = np.meshgrid(current_amplitude, area)

# Calculate the current density (mA/cm²)
Z = X / Y

# --- NEW: Print current density for specific values ---
specific_current = 0.3  # mA
specific_area = 3.0     # cm²
specific_density = specific_current / specific_area
print(f"Current Density for I = {specific_current} mA and A = {specific_area} cm²: {specific_density:.3f} mA/cm²")

exit()

# Create the filled contour plot, scaling the colors between 0 and 5
plt.figure(figsize=(4, 5))
cp = plt.contourf(X, Y, Z, levels=np.linspace(0, 5, 1000), cmap='jet', vmin=0, vmax=5)

# Create the colorbar with ticks from 0 to 5, in steps of 0.5
cbar = plt.colorbar(cp, ticks=np.arange(0, 5.5, 0.5))

# Set the colorbar label and its fontsize
cbar.set_label('Current Density (mA/cm²)', fontsize=12)  # Label fontsize
cbar.ax.tick_params(labelsize=11)  # Colorbar tick labels size

# Add black contour lines on top of the filled contour plot (Z < 0.5 as an example)
contour_lines = plt.contour(X, Y, Z, levels=[0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 1.0], colors='white', linewidths=1)

# Add labels to contour lines and store the label text objects
labels = plt.clabel(contour_lines, inline=True, fontsize=10)  # Add labels to the contour lines

# Set the font weight of each label to bold
for label in labels:
    label.set_fontweight('bold')

# Labeling the axes and title with fontsize 10
plt.title('Current Density (mA/cm²)', pad=20, fontsize=14)
plt.xlabel('Current Amplitude (mA)', fontsize=12)
plt.ylabel('Electrode Area (cm²)', fontsize=12)

# Adjust the tick parameters for both x and y axes
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)

# Tighten the layout
plt.tight_layout()

# plt.savefig('Corrigenda Figure 3-1 A.png', dpi=300)

# Display the plot
plt.show()
