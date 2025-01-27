import numpy as np
import matplotlib.pyplot as plt

# Define the parameters
current_amplitude = np.linspace(0.01, 0.5, 100)  # Peak-to-peak current in mA
duration = np.linspace(0.01, 0.5, 100)  # Duration of the pulse in seconds (total period)

# Create a meshgrid for current amplitude (X) and pulse duration (Y)
X, Y = np.meshgrid(current_amplitude, duration)

# Constants and formula for charge calculation
# I_peak is half the peak-to-peak current
I_peak = X / 2  # Convert to peak current in mA
t_half_phase = Y / 2  # Half the pulse duration (s)

# Convert I_peak to amperes (from mA)
I_peak = I_peak * 10**-3  # Convert mA to A

# I_RMS = I_peak / sqrt(2)
I_RMS = I_peak / np.sqrt(2)

# Calculate charge per phase: Charge = I_RMS * t_half-phase (in Coulombs)
charge_per_phase = I_RMS * t_half_phase

# Total charge per pulse (sum of both phases) in microCoulombs
charge_per_pulse = 2 * charge_per_phase * 10**6  # Convert to µC

# Create the filled contour plot for charge per pulse (µC)
plt.figure(figsize=(4, 5))
cp = plt.contourf(X, Y, charge_per_pulse, levels=np.linspace(0, 90, 90), cmap='jet', vmin=0, vmax=90)

# Create the colorbar with charge per pulse (µC) as the label
cbar = plt.colorbar(cp, label='Charge (µC)', ticks=np.linspace(0, 90, 10))
cbar.set_label('Charge (µC)', fontsize=12)  # Set colorbar label fontsize
cbar.ax.tick_params(labelsize=11)  # Set colorbar tick labels fontsize

# Add black contour lines on top of the filled contour plot
contour_lines = plt.contour(X, Y, charge_per_pulse, levels=[1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90], colors='white', linewidths=1)

# Add labels to contour lines and store the label text objects
labels = plt.clabel(contour_lines, inline=True, fontsize=10)  # Set contour labels fontsize

# Set the font weight of each label to bold
for label in labels:
    label.set_fontweight('bold')
    # Get current position and adjust it only for first label
    if label.get_text() == '1':
        x, y = label.get_position()
        label.set_position((x + 0.02, y - 0.1))


# Label the axes and title with fontsize 10
plt.title('Pulse total charge (µC)', pad=20, fontsize=14)
plt.xlabel('Current amplitude (mA)', fontsize=12)
plt.ylabel('Duration (s)', fontsize=12)

# Adjust the tick parameters for both x and y axes
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)

# Tighten the layout
plt.tight_layout()

# plt.savefig('figure 22b total charge.png', dpi=300)

# Display the plot
plt.show()
