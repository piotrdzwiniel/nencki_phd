import numpy as np
import matplotlib.pyplot as plt

# Time vector
t = np.linspace(0, 4 * np.pi, 1000)

# Low-frequency signal for phase modulation
low_freq_signal = np.sin(t)

# High-frequency signal with amplitude modulation
high_freq_signal = np.sin(10 * t) * np.sin(t)

# Decrease amplitude of high_freq_signal by 10 for negative values of low_freq_signal
high_freq_signal[low_freq_signal < 0] *= 0.01

# Create the figure and axis
fig, ax = plt.subplots(figsize=(5, 3))

# Plot high-frequency modulated signal (black)
ax.plot(t, high_freq_signal, color='black', linewidth=2)

# Plot low-frequency envelope (orange)
ax.plot(t, low_freq_signal, color='#5654FC', linewidth=2)

# Remove axis for visual similarity
ax.axis('off')

# Add the title
ax.set_title('Phase-amplitude coupling', fontsize=14)

# Display the plot
plt.show()
