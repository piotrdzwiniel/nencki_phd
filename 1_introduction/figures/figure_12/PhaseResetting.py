import numpy as np
import matplotlib.pyplot as plt

# Generate time vector from 0 to 2π with 500 points
t = np.linspace(0, 2 * np.pi, 500)

# Define signals before phase reset
# Three sinusoidal signals with different phase shifts
signal_before1 = np.sin(3 * t)
signal_before2 = np.sin(3 * t + np.pi / 4)  # Phase shift of π/4
signal_before3 = np.sin(3 * t + np.pi / 2)  # Phase shift of π/2

# Define signals after phase reset (reset to original phase)
# All signals have the same phase after reset
signal_after1 = np.sin(3 * t)
signal_after2 = np.sin(3 * t)
signal_after3 = np.sin(3 * t)

# Create the figure and axis with specified figure size
fig, ax = plt.subplots(figsize=(5, 3))

# Plot signals before the phase reset (first half of the time vector)
ax.plot(t[:len(t)//2], signal_before1[:len(t)//2], color='black', linewidth=2)
ax.plot(t[:len(t)//2], signal_before2[:len(t)//2] - 1, color='black', linewidth=2)  # Shift down by 1 for visual separation
ax.plot(t[:len(t)//2], signal_before3[:len(t)//2] - 2, color='black', linewidth=2)  # Shift down by 2 for visual separation

# Plot signals after the phase reset (second half of the time vector)
ax.plot(t[len(t)//2:], signal_after1[len(t)//2:], color='#5654FC', linewidth=2)
ax.plot(t[len(t)//2:], signal_after2[len(t)//2:] - 1, color='#5654FC', linewidth=2)
ax.plot(t[len(t)//2:], signal_after3[len(t)//2:] - 2, color='#5654FC', linewidth=2)

# Add vertical line to indicate phase reset point at π
ax.axvline(x=np.pi, color='#5654FC', linewidth=2)

# Remove axis for a cleaner visual representation
ax.axis('off')

# Add title to the plot
ax.set_title('Phase resetting', fontsize=14)

# Display the plot
plt.show()
