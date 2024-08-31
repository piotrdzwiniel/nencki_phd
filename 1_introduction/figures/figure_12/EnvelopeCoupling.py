import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import matplotlib.patches as patches

# Time vector
t = np.linspace(0, 4 * np.pi, 1000)

# High-frequency signals with different frequencies and phase shifts
high_freq_signal1 = np.sin(10 * t) * np.sin(t)
high_freq_signal2 = np.sin(12 * t + np.pi / 4) * np.sin(t)

# Low-frequency envelope (identical for both signals)
envelope = np.sin(t)

# Find peaks of the envelope for dashed line positions
peaks, _ = find_peaks(envelope)

# Create the figure and axis
fig, ax = plt.subplots(figsize=(5, 3))

# Plot vertical dashed lines at envelope peaks and rectangles
for peak in peaks:
    ax.axvspan(t[peak] - 0.5, t[peak] + 0.5, color='#5654FC', alpha=0.2)

# Plot high-frequency signals
ax.plot(t, high_freq_signal1, color='black', linewidth=2)
ax.plot(t, high_freq_signal2 - 2, color='black', linewidth=2)  # Shifted vertically

# Plot low-frequency envelopes (orange) for visual similarity
ax.plot(t, envelope + 1, color='#5654FC', linewidth=2)
ax.plot(t, envelope - 1, color='#5654FC', linewidth=2)

# Remove axis for visual similarity
ax.axis('off')

# Add the title
ax.set_title('Envelope coupling', fontsize=14)

# Display the plot
plt.show()
