import numpy as np
import matplotlib.pyplot as plt

# Time vector
t = np.linspace(0, 4 * np.pi, 1000)  # Creates a time vector from 0 to 4π with 1000 points

# Low-frequency signal for phase modulation
low_freq_signal = np.sin(t)  # A low-frequency sine wave signal

# High-frequency signal with amplitude modulation
high_freq_signal = np.sin(10 * t) * np.sin(t)  # A high-frequency sine wave modulated by a low-frequency sine wave

# Decrease amplitude of high_freq_signal by a factor of 100 for negative values of low_freq_signal
high_freq_signal[low_freq_signal < 0] *= 0.01  # Apply amplitude modulation based on the phase of the low-frequency signal

# Create the figure and axis
fig, ax = plt.subplots(figsize=(5, 3))  # Set up a figure with custom size 5x3 inches

# Plot the high-frequency modulated signal (black)
ax.plot(t, high_freq_signal, color='black', linewidth=2)  # Plot the high-frequency signal with phase-dependent amplitude

# Plot the low-frequency envelope (orange)
ax.plot(t, low_freq_signal, color='#5654FC', linewidth=2)  # Plot the low-frequency signal for reference

# Remove axis for visual similarity
ax.axis('off')  # Turn off the axis lines and labels for a cleaner visual

# Add the title
ax.set_title('Phase-Amplitude Coupling', fontsize=14)  # Title of the plot

# Display the plot
plt.show()  # Show the plot
