import numpy as np
import matplotlib.pyplot as plt

# Parameters
fs = 1000  # Sampling frequency
t = np.arange(0, 0.5, 1/fs)  # Time vector
f = 10  # Frequency of the sinusoid
amplitude = 1  # Amplitude of the sinusoid

# 1. Create the 10 Hz sinusoid signal
sinusoid = amplitude * np.sin(2 * np.pi * f * t)

# 2. Create a noisy signal (sinusoid + Gaussian noise)
noise = np.random.normal(0, 0.5, t.shape)
noisy_signal = sinusoid + noise

# 3. Calculate threshold crossings
max_value = np.max(sinusoid)
threshold_crossings = noisy_signal > max_value

# Create the figure and subplots
fig, (ax2, ax1) = plt.subplots(2, 1, figsize=(5, 4), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)

# Add the dashed horizontal line at the maximum of the sinusoid with label
ax2.axhline(y=max_value, color='black', linestyle='--')
ax2.text(t[-1], max_value, ' Threshold', color='black', va='bottom', ha='right', fontsize=9)

# Plot the noisy signal (light gray line) and sinusoid (bolded black line)
ax2.plot(t, noisy_signal, color='#5654FC', alpha=0.2)
ax2.plot(t, sinusoid, color='black', linewidth=2)

# Labels and title for the main plot
ax2.set_ylabel('Amplitude')
ax2.set_title('10 Hz sinusoid with gaussian noise', fontsize=10)

# Plot threshold crossing spikes
ax1.vlines(t[threshold_crossings], ymin=0, ymax=1, color='black')
ax1.set_ylim(0, 1)
ax1.set_yticks([])  # Remove y-axis ticks for spikes
ax1.set_xlabel('Time (s)')
ax1.set_title('Threshold crossing spikes', fontsize=10)

# Adjust layout to fit everything nicely
plt.tight_layout()

# Display the plot
plt.show()
