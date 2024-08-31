import numpy as np
import matplotlib.pyplot as plt

# Time vector
t = np.linspace(0, 2 * np.pi, 1000)  # Creates a time vector from 0 to 2π with 1000 points

# Signals with similar frequency but slightly different phase
signal1 = np.sin(5 * t)  # Sine wave with frequency 5 and no phase shift
signal2 = np.sin(5 * t + np.pi / 6)  # Sine wave with frequency 5, phase shifted by π/6
signal3 = signal1 + signal2  # Combined signal, sum of signal1 and signal2

# Create the figure and axis
fig, ax = plt.subplots(figsize=(5, 3))  # Set up a figure with custom size 5x3 inches

# Plot the signals
ax.plot(t, signal1 + 1, color='black', linewidth=2)  # Plot signal1, shifted vertically for clarity
ax.plot(t, signal2 - 1, color='black', linewidth=2)  # Plot signal2, shifted vertically for clarity
ax.plot(t, signal3 / 2, color='#5654FC', linewidth=2)  # Plot the combined signal, scaled down

# Find the positions of maxima for both sine waves
max_indices_signal1 = np.where(np.diff(np.sign(np.diff(signal1))) < 0)[0] + 1
max_positions_signal1 = t[max_indices_signal1]  # Time positions of maxima in signal1

max_indices_signal2 = np.where(np.diff(np.sign(np.diff(signal2))) < 0)[0] + 1
max_positions_signal2 = t[max_indices_signal2]  # Time positions of maxima in signal2

# Ensure both signals have the same number of maxima (just in case)
num_maxima = min(len(max_positions_signal1), len(max_positions_signal2))

# Plot shaded rectangles from maxima of signal2 to corresponding maxima of signal1
for i in range(num_maxima):
    start = max_positions_signal2[i]
    end = max_positions_signal1[i]
    ax.axvspan(start-0.1, end+0.1, color='#5654FC', alpha=0.2)  # Shaded area between maxima

# Remove axis for visual simplicity
ax.axis('off')  # Turn off the axis lines and labels for a cleaner visual

# Add the title
ax.set_title('Phase Coupling', fontsize=14)  # Title of the plot

# Display the plot
plt.show()  # Show the plot
