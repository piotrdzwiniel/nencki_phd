import numpy as np
import matplotlib.pyplot as plt

# Parameters for the sinusoid
frequency = 10  # Frequency in Hz
duration = 1  # Duration in seconds
amplitude_pp = 20  # Peak-to-peak amplitude in microamperes (20 µA)
sampling_rate = 1000  # Sampling rate in Hz

# Time vector for 1 second
t = np.linspace(0, duration, int(sampling_rate * duration))

# Generate the 10 Hz sinusoidal signal with the specified peak-to-peak amplitude
# Amplitude in terms of peak value is half of peak-to-peak value
amplitude_peak = amplitude_pp / 2  # Convert to microamperes (already in µA)
signal = amplitude_peak * np.sin(2 * np.pi * frequency * t)

# Create the figure and axis
fig, ax = plt.subplots(figsize=(4, 2))

# Plot the signal
ax.plot(t, signal, color='black', linewidth=2)

# Customize the axes
ax.set_xlabel("Time (s)")
ax.set_ylabel("Current (µA)")  # Label in microamperes

# Set the title
ax.set_title("10 Hz stimulation signal", fontsize=10)

# Only show x and y axes
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(True)
ax.spines['bottom'].set_visible(True)

# Set the y-axis limits with additional space above and below the signal curve
padding = amplitude_peak * 0.2  # 20% padding for better visibility
ax.set_ylim([-amplitude_peak - padding, amplitude_peak + padding])

# Display the plot
plt.tight_layout()
plt.show()
