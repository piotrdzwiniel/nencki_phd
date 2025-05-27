import numpy as np
import matplotlib.pyplot as plt

# Define the parameters
current_amplitude = np.linspace(0.01, 0.5, 100)  # Peak-to-peak current in mA
duration = np.linspace(0.01, 0.5, 100)  # Duration of the pulse in seconds (total period)

# Create a meshgrid for current amplitude (X) and pulse duration (Y)
X, Y = np.meshgrid(current_amplitude, duration)

def total_charge(d, A):
    """
    Calculate the total charge of a current pulse.

    Parameters:
    - d: Pulse duration in milliseconds (ms).
    - A: Pulse amplitude in microamperes (µA).

    Returns:
    - Total charge in microcoulombs (µC).
    """
    # d in ms, A in µA
    I_pp = A / 1e6  # Peak-to-peak current in amperes (100 µA)
    I_peak = I_pp / 2  # Peak current in amperes
    T_pulse = d / 1e3  # Total pulse duration in seconds (100 ms)
    f = 1 / T_pulse  # Frequency in Hz (assuming full sinusoid fits in pulse duration)

    Q_pulse_analytic_uC = (2 * I_peak) / (np.pi * f) * 1e6
    return Q_pulse_analytic_uC


charge_per_pulse = total_charge(Y, X) * 10**6

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
plt.title('Total Charge (µC)', pad=20, fontsize=14)
plt.xlabel('Current Amplitude (mA)', fontsize=12)
plt.ylabel('Duration (s)', fontsize=12)

# Adjust the tick parameters for both x and y axes
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)

# Tighten the layout
plt.tight_layout()

# plt.savefig('Corrigenda Figure 3-1 B.png', dpi=300)

# Display the plot
plt.show()
