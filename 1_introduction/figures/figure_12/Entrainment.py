import numpy as np
import matplotlib.pyplot as plt

# Time vector
t = np.linspace(0, 2 * np.pi, 500)  # Creates a time vector from 0 to 2π with 500 points

# Signal
signal = np.sin(3 * t) / 2  # Sine wave signal with a frequency multiplier of 3, scaled by 0.5

# Create the figure and axis
fig, ax = plt.subplots(figsize=(5, 3))  # Set up a figure with custom size 5x3 inches

# Plot the signal
ax.plot(t, signal, color='black', linewidth=2)  # Plot the sine wave

# Plot vertical lines
for i in range(1, 4):
    ax.axvline(x=(i * np.pi / 1.5) - 2, color='#5654FC', linewidth=4, ymin=0.8, ymax=0.9)
    # Vertical lines at calculated positions with specific ymin and ymax for line height

# Remove axis for visual similarity
ax.axis('off')  # Turn off the axis lines and labels for a cleaner look
ax.set_ylim(-1, 1)  # Set the y-axis limits to keep the signal within bounds

# Add the title
ax.set_title('Entrainment', fontsize=14)  # Title of the plot

# Display the plot
plt.show()  # Show the plot
