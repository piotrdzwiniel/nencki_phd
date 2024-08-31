import numpy as np
import matplotlib.pyplot as plt

# Parameters for the signal
fs = 1000  # Sampling frequency in Hz
t = np.arange(0, 0.5, 1/fs)  # Time vector from 0 to 0.5 seconds with step size 1/fs
f = 10  # Frequency of the sinusoid in Hz
amplitude = 1  # Amplitude of the sinusoid

# 1. Create the 10 Hz sinusoidal signal
sinusoid = amplitude * np.sin(2 * np.pi * f * t)

# 2. Create a noisy signal by adding Gaussian noise to the sinusoid
noise = np.random.normal(0, 0.5, t.shape)  # Gaussian noise with mean 0 and standard deviation 0.5
noisy_signal = sinusoid + noise  # Noisy signal is the sum of the sinusoid and noise

# 3. Calculate threshold crossings where the noisy signal exceeds the maximum value of the sinusoid
max_value = np.max(sinusoid)  # Maximum amplitude of the sinusoid
threshold_crossings = noisy_signal > max_value  # Boolean array for threshold crossings

# Create the figure and subplots
fig, (ax2, ax1) = plt.subplots(2, 1, figsize=(5, 4), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)

# Add a dashed horizontal line at the maximum of the sinusoid with a label indicating the threshold
ax2.axhline(y=max_value, color='black', linestyle='--')
ax2.text(t[-1], max_value, ' Threshold', color='black', va='bottom', ha='right', fontsize=9)

# Plot the noisy signal in a light color for background visibility
ax2.plot(t, noisy_signal, color='#5654FC', alpha=0.2)

# Plot the original sinusoidal signal with a bold black line
ax2.plot(t, sinusoid, color='black', linewidth=2)

# Set labels and title for the main plot
ax2.set_ylabel('Amplitude')
ax2.set_title('10 Hz sinusoid with Gaussian noise', fontsize=10)

# Plot threshold crossing spikes
ax1.vlines(t[threshold_crossings], ymin=0, ymax=1, color='black')

# Customize the lower plot showing threshold crossings
ax1.set_ylim(0, 1)  # Set y-axis limits to clearly show spikes
ax1.set_yticks([])  # Remove y-axis ticks for a cleaner appearance
ax1.set_xlabel('Time (s)')
ax1.set_title('Threshold crossing spikes', fontsize=10)

# Adjust layout to fit all elements nicely without overlapping
plt.tight_layout()

# Display the plot
plt.show()
