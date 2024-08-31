import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.signal import find_peaks
import Utils as ut  # Custom utility module, ensure it is available and correctly implemented

# Set parameters for the signals
frequency_vis = 11  # Frequency in Hz for the visual signal (entrainment)
frequency_novis = 10  # Frequency in Hz for the non-visual signal (no entrainment)
amplitude = 0.3  # Scaling factor for visualizing the amplitude of the signals

# Create a time vector using the custom utility function
# Generates a time vector from 0 to 0.5 seconds, sampled at 1000 Hz
t = ut.create_time_scale(500, 1000, 's')

# Generate low-frequency sinusoidal signals for modulation
low_freq_signal_vis = np.sin(2 * np.pi * frequency_vis * t)  # For the visual signal (entrainment)
low_freq_signal_novis = np.sin(2 * np.pi * frequency_novis * t)  # For the non-visual signal (no entrainment)

# Generate a high-frequency random noise signal, centered around zero
high_freq_signal = np.random.randn(len(t))

# Apply amplitude modulation to the high-frequency signal using the non-visual low-frequency signal
high_freq_signal *= low_freq_signal_novis

# Shift low-frequency signals up to avoid negative values
low_freq_signal_vis += 2
low_freq_signal_novis += 2

# Adjust the high-frequency signal based on the low-frequency signal values
# Reduce amplitude where the non-visual low-frequency signal is below a threshold
high_freq_signal[low_freq_signal_novis < 2] *= 0.1

# Center the high-frequency signal around zero after modulation
high_freq_signal -= 2

# Create a figure and axis for plotting
fig, ax = plt.subplots(figsize=(6, 2.5))

# Define a colormap for the background gradient (white to light gray)
cmap = mcolors.LinearSegmentedColormap.from_list('white_to_gray', ['white', (200/255, 200/255, 200/255, 1)])

# Generate gradient data for background visualization
gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))

# Rotate the gradient 90 degrees clockwise for visual effect
rotated_gradient = np.rot90(gradient, k=-1)

# Display the rotated gradient as the background of the plot
ax.imshow(rotated_gradient, aspect='auto', cmap=cmap, extent=[t.min(), t.max(), -4, 3])

# Detect peaks in the inverted non-visual low-frequency signal to identify regions of interest
peaks_novis, _ = find_peaks(-low_freq_signal_novis)

# Highlight regions around detected peaks with shaded areas
for peak in peaks_novis:
    ax.axvspan(t[peak] - 0.025, t[peak] + 0.025, color='white', alpha=1.0)

# Detect peaks in the visual low-frequency signal for additional markers
peaks_vis, _ = find_peaks(low_freq_signal_vis)

# Plot vertical dashed lines at detected peaks of the visual low-frequency signal
for peak in peaks_vis:
    plt.axvline(x=t[peak], color='#5654FC', alpha=1, linestyle='dashed')
    print(f"Peak detected at: {t[peak]:.3f} seconds")

# Plot the high-frequency modulated signal in black
ax.plot(t, high_freq_signal, color='black', linewidth=2)

# Plot the visual low-frequency envelope signal in blue
ax.plot(t, low_freq_signal_vis * amplitude, color='#5654FC', linewidth=2)

# Customize the axis appearance for better visual presentation
ax.set_title('No Entrainment', fontsize=14)
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
