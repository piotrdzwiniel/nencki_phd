# Amplitude modulation
import numpy as np
import matplotlib.pyplot as plt

# Time vector
t = np.linspace(0, 2 * np.pi, 500)

# Signal before modulation
signal_before = np.sin(4 * t)

# Signal after modulation
signal_after = 2 * np.sin(4 * t)

# Create the figure and axis
fig, ax = plt.subplots(figsize=(5, 3))

# Plot the signals
ax.plot(t[:len(t)//2], signal_before[:len(t)//2], color='black', linewidth=2)
ax.plot(t[len(t)//2:], signal_after[len(t)//2:], color='#5654FC', linewidth=2)

# Add vertical line to separate the two segments
ax.axvline(x=np.pi, color='#5654FC', linewidth=2)

# Remove axis for visual similarity
ax.axis('off')

# Add the title
ax.set_title('Amplitude modulation', fontsize=14)

# Display the plot
plt.show()
