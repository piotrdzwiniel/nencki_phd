import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.signal import find_peaks

# Determine the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go two folders up
two_folders_up = os.path.abspath(os.path.join(current_dir, '../../'))

# Add the two-folders-up path to the system path
sys.path.insert(0, two_folders_up)

import Utils as ut  # Custom utility module, ensure this is correctly implemented and accessible

# Set up parameters for the low-frequency signal
frequency = 9  # Frequency in Hz for the low-frequency sinusoidal signal
amplitude = 0.9  # Scaling factor for visualizing the amplitude of the signals

# Create a time vector using a custom utility function
# Generates a time vector from 0 to 0.5 seconds, sampled at 1000 Hz
t = ut.create_time_scale(500, 1000, 's')

# Generate a low-frequency sinusoidal signal for phase modulation
low_freq_signal = np.sin(2 * np.pi * frequency * t)

# Generate a high-frequency random noise signal centered around zero
high_freq_signal = np.random.randn(len(t))

# Apply amplitude modulation to the high-frequency signal using the low-frequency signal
high_freq_signal *= low_freq_signal

# Shift the low-frequency signal up to ensure non-negative values
low_freq_signal += 2

# Adjust the amplitude of the high-frequency signal based on the low-frequency signal values
# Reduce amplitude where the low-frequency signal is below a threshold
high_freq_signal[low_freq_signal < 2] *= 0.1

# Center the high-frequency signal around zero after modulation
high_freq_signal -= 2

# Create a figure and axis for plotting
fig, ax = plt.subplots(figsize=(6, 2.5))

# Define a colormap for a background gradient transitioning from white to blue
cmap = mcolors.LinearSegmentedColormap.from_list('white_to_blue', ['white', (86/255, 84/255, 252/255, 0.25)])

# Generate gradient data for the background visualization
gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))

# Rotate the gradient 90 degrees clockwise for visual effect
rotated_gradient = np.rot90(gradient, k=-1)

# Display the rotated gradient as the background of the plot
ax.imshow(rotated_gradient, aspect='auto', cmap=cmap, extent=[t.min(), t.max(), -4, 3])

# Detect peaks in the inverted low-frequency signal to identify regions of interest
peaks, _ = find_peaks(-low_freq_signal)

# Highlight regions around detected peaks with shaded areas
for peak in peaks:
    ax.axvspan(t[peak] - 0.025, t[peak] + 0.025, color='white', alpha=1.0)

# Detect peaks in the low-frequency signal for additional markers
peaks, _ = find_peaks(low_freq_signal)

# Plot vertical dashed lines at detected peaks of the low-frequency signal
for peak in peaks:
    plt.axvline(x=peak / 1000, color='#5654FC', alpha=1, linestyle='dashed')

# Plot the high-frequency modulated signal in black
ax.plot(t, high_freq_signal, color='black', linewidth=2)

# Plot the low-frequency envelope signal in blue
ax.plot(t, low_freq_signal * amplitude, color='#5654FC', linewidth=2)

# Customize the axis appearance for better visual presentation
ax.set_title('Entrainment', fontsize=14)
ax.set_xlabel("Time (s)")

# Remove unnecessary axis spines to simplify the plot
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)

# Keep the bottom spine visible for the x-axis
ax.spines['bottom'].set_visible(True)

# Remove y-axis ticks and labels for a cleaner look
ax.yaxis.set_ticks([])
ax.yaxis.set_ticklabels([])

# Set y-axis limits to ensure all signals are within the viewable area
ax.set_ylim([-4, 4])
ax.set_xlim([0.0, 0.5])  # Set x-axis limits to match the time vector

# Adjust layout for better spacing and presentation
plt.tight_layout()

# Display the plot
plt.show()
