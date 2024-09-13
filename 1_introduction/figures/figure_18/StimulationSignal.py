import numpy as np
import matplotlib.pyplot as plt

# Parameters for the sinusoidal signal
frequency = 10  # Frequency of the sinusoid in Hz
duration = 1  # Duration of the signal in seconds
amplitude_pp = 20  # Peak-to-peak amplitude in microamperes (µA)
sampling_rate = 1000  # Sampling rate in Hz

# Generate a time vector for 1 second, sampled at the specified rate
t = np.linspace(0, duration, int(sampling_rate * duration))

# Compute the peak amplitude from the peak-to-peak value
amplitude_peak = amplitude_pp / 2  # Half of the peak-to-peak amplitude in microamperes

# Generate the sinusoidal signal at 10 Hz with the computed peak amplitude
signal = amplitude_peak * np.sin(2 * np.pi * frequency * t)

# Create the figure and axis for plotting
fig, ax = plt.subplots(figsize=(4, 2))

# Plot the generated sinusoidal signal
ax.plot(t, signal, color='black', linewidth=2)

# Customize the axes labels
ax.set_xlabel("Time (s)")
ax.set_ylabel("Current (µA)")  # Y-axis label indicating current in microamperes

# Set the title of the plot
ax.set_title("10 Hz stimulation signal", fontsize=10)

# Only show x and y axes; hide the top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(True)
ax.spines['bottom'].set_visible(True)

# Set the y-axis limits to provide padding for better visibility of the signal
padding = amplitude_peak * 0.2  # 20% of the peak amplitude as padding
ax.set_ylim([-amplitude_peak - padding, amplitude_peak + padding])

# Adjust layout for a cleaner appearance
plt.tight_layout()

# Display the plot
plt.show()
