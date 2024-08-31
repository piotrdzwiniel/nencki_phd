import numpy as np
import matplotlib.pyplot as plt

# Time vector
t = np.linspace(0, 2 * np.pi, 1000)

# Signals with similar frequency but slightly different phase
signal1 = np.sin(5 * t)
signal2 = np.sin(5 * t + np.pi / 6)  # Phase shifted by pi/6
signal3 = signal1 + signal2

# Create the figure and axis
fig, ax = plt.subplots(figsize=(5, 3))

# Plot the signals
ax.plot(t, signal1 + 1, color='black', linewidth=2)
ax.plot(t, signal2 - 1, color='black', linewidth=2)  # Shifted vertically for separation
ax.plot(t, signal3 / 2, color='#5654FC', linewidth=2)  # Shifted vertically for separation

# Find the positions of maxima for both sine waves
max_indices_signal1 = np.where(np.diff(np.sign(np.diff(signal1))) < 0)[0] + 1
max_positions_signal1 = t[max_indices_signal1]

max_indices_signal2 = np.where(np.diff(np.sign(np.diff(signal2))) < 0)[0] + 1
max_positions_signal2 = t[max_indices_signal2]

# Ensure both signals have the same number of maxima (just in case)
num_maxima = min(len(max_positions_signal1), len(max_positions_signal2))

# Plot orange rectangles from maxima of signal2 to corresponding maxima of signal1
for i in range(num_maxima):
    start = max_positions_signal2[i]
    end = max_positions_signal1[i]
    ax.axvspan(start-0.1, end+0.1, color='#5654FC', alpha=0.2)

# Remove axis for visual simplicity
ax.axis('off')

# Add the title
ax.set_title('Phase coupling', fontsize=14)

# Display the plot
plt.show()

