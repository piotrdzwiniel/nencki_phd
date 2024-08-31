import numpy as np
import matplotlib.pyplot as plt

# Time vector
t = np.linspace(0, 2 * np.pi, 500)

# Signal
signal = np.sin(3 * t) / 2

print(signal)


# Create the figure and axis
fig, ax = plt.subplots(figsize=(5, 3))

# Plot the signal
ax.plot(t, signal, color='black', linewidth=2)

# Plot vertical lines
for i in range(1, 4):
    ax.axvline(x=(i * np.pi / 1.5) - 2, color='#5654FC', linewidth=4, ymin=0.8, ymax=0.9)

# Remove axis for visual similarity
ax.axis('off')
ax.set_ylim(-1, 1)

# Add the title
ax.set_title('Entrainment', fontsize=14)

# Display the plot
plt.show()
