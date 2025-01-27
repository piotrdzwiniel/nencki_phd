import numpy as np
import matplotlib.pyplot as plt
import Utils as ufe  # Custom module for EEG utilities

# Load VEP (Visual Evoked Potentials) data
vep = np.load("VEP.npy")

# Define parameters for identifying specific points in the VEP signal
c = 0  # Offset adjustment (default 0)
n1 = np.min(vep[925 + c:975 + c])  # First negative peak (N1) within specified range
p1 = np.max(vep[950 + c:1000 + c])  # First positive peak (P1) within specified range
n2 = np.min(vep[1005 + c:1055 + c])  # Second negative peak (N2) within specified range

# Create the first subplot for plotting
fig, ax1 = plt.subplots()

# Plot the current pulse on the first y-axis
current_pulse, _ = ufe.create_sin_pulse(10.0, 1000, 100.0)  # Create sinusoidal pulse data

timeline_cs = np.arange(-100, 0, 1)  # Define time range for the current pulse
ax1.plot(timeline_cs, current_pulse, color='black', label='pCS time course')  # Plot the pulse

# Highlight pulse regions before and after -50 ms
plt.fill_between(timeline_cs, current_pulse, where=timeline_cs <= -50, color='r', alpha=0.8)  # Red region
plt.fill_between(timeline_cs, current_pulse, where=timeline_cs > -50, color=(0, 0.502, 1), alpha=0.8)  # Blue region

# Configure the first y-axis
ax1.set_xlabel('Time (ms)')
ax1.set_ylabel('Current Pulse Amplitude (µA)', color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.set_ylim(-50.0, 50.0)  # Set y-axis limits

# Create a second y-axis for plotting VEP data
ax2 = ax1.twinx()  # Share the same x-axis

# Plot the VEP data on the second y-axis
ax2.plot(np.arange(0, 1126, 1), vep[875:], color='black', linestyle='-.', label='VEP time course')
ax2.set_ylabel('Visual Evoked Potential Amplitude (µV)', color='black')
ax2.tick_params(axis='y', labelcolor='black')
ax2.axvline(0, linewidth=2, color='black', linestyle='--', label="CPR onset")  # Mark CPR onset
ax2.set_ylim(-0.6, 0.6)  # Set y-axis limits for VEP plot

# Add legends for both axes
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines = lines1 + lines2
labels = labels1 + labels2
ax1.legend(lines, labels, loc='upper right')

# Show the plot
plt.xlim([-100, 500])  # Set x-axis limits
# plt.savefig("ForFigure1.png", dpi=300)  # Optionally save the figure
plt.show()
