import numpy as np
import matplotlib.pyplot as plt

# Time vector
t = np.linspace(0, 2 * np.pi, 500)  # Creates a time vector from 0 to 2π with 500 points

# Signal before modulation
signal_before = np.sin(4 * t)  # Original signal (sine wave with a frequency multiplier of 4)

# Signal after modulation
signal_after = 2 * np.sin(4 * t)  # Modulated signal (amplitude doubled)

# Create the figure and axis
fig, ax = plt.subplots(figsize=(5, 3))  # Set up a figure with custom size 5x3 inches

# Plot the signals
ax.plot(t[:len(t)//2], signal_before[:len(t)//2], color='black', linewidth=2)  # Plot the original signal in the first half
ax.plot(t[len(t)//2:], signal_after[len(t)//2:], color='#5654FC', linewidth=2)  # Plot the modulated signal in the second half

# Add vertical line to separate the two segments
ax.axvline(x=np.pi, color='#5654FC', linewidth=2)  # Vertical line at t = π to distinguish between before and after modulation

# Remove axis for visual similarity
ax.axis('off')  # Turn off the axis lines and labels for a cleaner look

# Add the title
ax.set_title('Amplitude Modulation', fontsize=14)  # Title of the plot

# Display the plot
plt.show()  # Show the plot
