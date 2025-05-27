import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter

# Define the ranges
charge = np.linspace(0.1, 50, 100)  # Charge in µC (X)
area = np.linspace(0.1, 5, 100)     # Area in cm² (Y)
num_pulses = np.linspace(1, 1000, 100)  # Number of pulses (Z)
result = (charge / area) * num_pulses # Color

# Create a meshgrid for charge and area
X, Y = np.meshgrid(charge, area)

# Compute the surface values
Z = (X / Y) * num_pulses[:, np.newaxis]  # Use broadcasting to match dimensions

# Create a figure and a 3D axis
fig = plt.figure(figsize=(6, 5))
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
surf = ax.plot_surface(X, Y, Z, cmap='jet', vmin=0, vmax=10000)

# Add labels and title
ax.set_xlabel('Charge (µC)', fontsize=12)
ax.set_ylabel('Electrode area (cm²)', fontsize=12)
ax.set_zlabel('Number of pulses (n)', fontsize=12)
ax.set_title('Pulse stimulation total charge (µC/cm²)', fontsize=14, pad=10)

# Invert the x-axis
ax.invert_xaxis()

# Add a color bar and adjust its position and size
cbar = fig.colorbar(surf, ax=ax, pad=0.15, shrink=0.5, aspect=10)
cbar.set_label('Total charge (µC/cm²)', fontsize=12)  # Set colorbar label fontsize
cbar.ax.tick_params(labelsize=11)  # Set colorbar tick labels fontsize

# Calculate Z values for custom ticks
num_pulses_values = [200, 400, 600, 800, 1000]
average_charge = (charge[0] + charge[-1]) / 2
average_area = (area[0] + area[-1]) / 2
average_ratio = average_charge / average_area

# Compute Z values for these num_pulses
custom_ticks = [average_ratio * n for n in num_pulses_values]

# Define custom labels for Z
custom_labels = [f'{n}' for n in num_pulses_values]

# Set custom ticks and labels on Z axis
ax.zaxis.set_major_locator(FixedLocator(custom_ticks))
ax.zaxis.set_major_formatter(FixedFormatter(custom_labels))

# Adjust the view angle to make the Z axis perpendicular if needed
# ax.view_init(elev=90, azim=-90)

# Adjust font size for ticks on x, y, and z axes
ax.tick_params(axis='both', which='major', labelsize=11)

plt.tight_layout()

# plt.savefig('figure 22c stimulation total charge.png', dpi=300)

# Show the plot
plt.show()
