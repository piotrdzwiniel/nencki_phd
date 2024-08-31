import numpy as np
import matplotlib.pyplot as plt

# Time vector
t = np.linspace(0, 2 * np.pi, 500)

# Signals before phase reset
signal_before1 = np.sin(3 * t)
signal_before2 = np.sin(3 * t + np.pi / 4)
signal_before3 = np.sin(3 * t + np.pi / 2)

# Signals after phase reset
signal_after1 = np.sin(3 * t)
signal_after2 = np.sin(3 * t)
signal_after3 = np.sin(3 * t)

# Create the figure and axis
fig, ax = plt.subplots(figsize=(5, 3))

# Plot signals before the phase reset
ax.plot(t[:len(t)//2], signal_before1[:len(t)//2], color='black', linewidth=2)
ax.plot(t[:len(t)//2], signal_before2[:len(t)//2] - 1, color='black', linewidth=2)
ax.plot(t[:len(t)//2], signal_before3[:len(t)//2] - 2, color='black', linewidth=2)

# Plot signals after the phase reset (reset to original phase at vertical line)
ax.plot(t[len(t)//2:], signal_after1[len(t)//2:], color='#5654FC', linewidth=2)
ax.plot(t[len(t)//2:], signal_after2[len(t)//2:] - 1, color='#5654FC', linewidth=2)
ax.plot(t[len(t)//2:], signal_after3[len(t)//2:] - 2, color='#5654FC', linewidth=2)

# Add vertical line to indicate phase reset point
ax.axvline(x=np.pi, color='#5654FC', linewidth=2)

# Remove axis for visual similarity
ax.axis('off')

# Add the title
ax.set_title('Phase resetting', fontsize=14)

# Display the plot
plt.show()
