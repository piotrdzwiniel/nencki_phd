import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import matplotlib.patches as patches

# Time vector
t = np.linspace(0, 4 * np.pi, 1000)  # Creates a time vector from 0 to 4π with 1000 points

# High-frequency signals with different frequencies and phase shifts
high_freq_signal1 = np.sin(10 * t) * np.sin(t)  # High-frequency signal 1 modulated by a low-frequency sine wave
high_freq_signal2 = np.sin(12 * t + np.pi / 4) * np.sin(t)  # High-frequency signal 2 with a phase shift and modulation

# Low-frequency envelope (identical for both signals)
envelope = np.sin(t)  # Low-frequency envelope used for both signals

# Find peaks of the envelope for dashed line positions
peaks, _ = find_peaks(envelope)  # Detect peaks in the envelope

# Create the figure and axis
fig, ax = plt.subplots(figsize=(5, 3))  # Set up a figure with a custom size of 5x3 inches

# Plot shaded rectangles around the envelope peaks
for peak in peaks:
    ax.axvspan(t[peak] - 0.5, t[peak] + 0.5, color='#5654FC', alpha=0.2)
    # Plot shaded areas around each peak with a width of 1 unit

# Plot high-frequency signals
ax.plot(t, high_freq_signal1, color='black', linewidth=2)  # Plot the first high-frequency signal
ax.plot(t, high_freq_signal2 - 2, color='black', linewidth=2)  # Plot the second high-frequency signal, shifted vertically

# Plot low-frequency envelopes (orange) for visual similarity
ax.plot(t, envelope + 1, color='#5654FC', linewidth=2)  # Plot the envelope above the first signal
ax.plot(t, envelope - 1, color='#5654FC', linewidth=2)  # Plot the envelope below the second signal

# Remove axis for visual similarity
ax.axis('off')  # Turn off the axis lines and labels for a cleaner visual

# Add the title
ax.set_title('Envelope Coupling', fontsize=14)  # Title of the plot

# Display the plot
plt.show()  # Show the plot
