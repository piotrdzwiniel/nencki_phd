import numpy as np
import matplotlib.pyplot as plt

# Load VEP (Visual Evoked Potential) data from files
veps = []  # Initialize an empty list to store VEP data arrays
for i in np.arange(15):
    # Load experimental VEP data for subjects EX_S1 to EX_S15
    veps.append(np.load("data_for_visualization/EX_S%d.npy" % (i + 1)))

for i in np.arange(16):
    # Load sham VEP data for subjects SH_S1 to SH_S16
    veps.append(np.load("data_for_visualization/SH_S%d.npy" % (i + 1)))

# Convert the list of VEP arrays into a single NumPy array
veps = np.asarray(veps)
# Calculate the average VEP across all loaded subjects
vep = np.average(veps, axis=0)

# Define an offset adjustment (currently set to 0)
c = 0

# Identify peaks in the VEP signal:
# N1 - first negative peak within the range 925-975 ms
n1 = np.min(vep[925 + c:975 + c])
# P1 - first positive peak within the range 950-1000 ms
p1 = np.max(vep[950 + c:1000 + c])
# N2 - second negative peak within the range 1005-1055 ms
n2 = np.min(vep[1005 + c:1055 + c])

# Create a figure and axes for plotting
fig = plt.figure(figsize=(8, 5))
ax = plt.subplot(111)

# Customize the appearance of plot borders
ax.spines['top'].set_visible(False)  # Hide the top spine
ax.spines['right'].set_visible(False)  # Hide the right spine
ax.spines['left'].set_linewidth(2.0)  # Set line width for the left spine
ax.spines['bottom'].set_linewidth(2.0)  # Set line width for the bottom spine

# Set axis labels and their font sizes
ax.set_xlabel('Time (ms)', fontsize=18)
ax.set_ylabel('Amplitude (Z-Score)', fontsize=18)
ax.tick_params(labelsize=18)  # Set the size of tick labels

# Plot a vertical line at 0 ms to indicate the onset of visual stimulation
plt.axvline(0, linewidth=2, color='black', linestyle='--', label="Visual Stimulation")
# Highlight the region representing current stimulation (-100 ms to 0 ms)
plt.axvspan(-100 + c, 0 + c, alpha=0.2, color="black", label="Current Stimulation")

# Plot the VEP data
plt.plot(np.arange(-875, 1126, 1), vep, label="VEP", color="black")

# Mark and label N1, P1, and N2 peaks on the plot
n1p1n2 = [
    [50 + np.argmin(vep[925 + c:975 + c]) + c, n1],  # N1 peak
    [75 + np.argmax(vep[950 + c:1000 + c]) + c, p1],  # P1 peak
    [130 + np.argmin(vep[1005 + c:1055 + c]) + c, n2]  # N2 peak
]
# Plot markers for the peaks
plt.plot(n1p1n2[0][0], n1p1n2[0][1], marker='o', color='#1F77B4', ls='', label="N1 (N75)", markersize=10)
plt.plot(n1p1n2[1][0], n1p1n2[1][1], marker='o', color='#FF7F0E', ls='', label="P1 (P100)", markersize=10)
plt.plot(n1p1n2[2][0], n1p1n2[2][1], marker='o', color='#D02627', ls='', label="N2 (N145)", markersize=10)

# Set x-axis limits for the plot
plt.xlim([-100, 500])

# Add a legend with specified font size
plt.legend(fontsize=18)

# Optimize the layout to prevent clipping
plt.tight_layout()

# Display the plot
plt.show()
