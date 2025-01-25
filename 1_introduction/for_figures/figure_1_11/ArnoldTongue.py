import matplotlib.pyplot as plt
import numpy as np

# Define frequency and strength ranges for the plot
freq = np.linspace(8, 12, 400)  # Frequency range from 8 to 12 Hz with 400 points
strength = np.linspace(0, 100, 400)  # Strength range from 0 to 100% with 400 points

# Create a meshgrid for contour plotting
X, Y = np.meshgrid(freq, strength)  # Meshgrid to represent the frequency-strength grid

# Initialize a matrix Z to represent the Arnold tongue region
Z = np.zeros_like(X)  # Matrix Z initialized with zeros, having the same shape as X

# Define the Arnold tongue region by setting Z to 1 within specific frequency boundaries
# The boundaries are set such that the frequency range narrows as strength increases
Z[(X >= 10 - (Y / 100) * 2) & (X <= 10 + (Y / 100) * 2)] = 1

# Create a figure for plotting
plt.figure(figsize=(4, 5))  # Set figure size to 4x5 inches

# Plot the Arnold tongue region using contourf (filled contour plot)
plt.contourf(X, Y, Z, levels=[0, 0.5, 1], colors=[
             (230/255, 230/255, 230/255, 1), (86/255, 84/255, 252/255, 0.25)])  # Light gray outside, light blue inside

# Plot first data point and crosshair
plt.scatter(9, 90, s=10, color='black')  # Mark a point at (9 Hz, 90%) in black
plt.plot([9, 9], [0, 90], color='black', alpha=0.25, linestyle='dashed')  # Vertical dashed line up to the point
plt.plot([8, 9], [90, 90], color='black', alpha=0.25, linestyle='dashed')  # Horizontal dashed line up to the point

# Plot second data point and crosshair
plt.scatter(11, 30, s=10, color='black')  # Mark a point at (11 Hz, 30%) in black
plt.plot([11, 11], [0, 30], color='black', alpha=0.25, linestyle='dashed')  # Vertical dashed line up to the point
plt.plot([8, 11], [30, 30], color='black', alpha=0.25, linestyle='dashed')  # Horizontal dashed line up to the point

# Add annotations to the plot
plt.text(10, 50, 'entrainment', horizontalalignment='center', verticalalignment='center',
         fontsize=12, color='black')  # Center text indicating 'entrainment' region
plt.text(8.5, 50, 'no entrainment', horizontalalignment='center', verticalalignment='center',
         fontsize=12, color='black', rotation=90)  # Vertical text indicating 'no entrainment' region on the left
plt.text(11.5, 50, 'no entrainment', horizontalalignment='center', verticalalignment='center',
         fontsize=12, color='black', rotation=90)  # Vertical text indicating 'no entrainment' region on the right

# Add labels and title to the plot
plt.xlabel('Frequency (Hz)')  # X-axis label
plt.ylabel('Strength (%)')  # Y-axis label
plt.title('Arnold Tongue', fontsize=14)  # Plot title

# Set limits for the x and y axes
plt.xlim(8, 12)  # X-axis range from 8 to 12 Hz
plt.ylim(0, 100)  # Y-axis range from 0 to 100%

# Define y-axis ticks at intervals of 10
plt.yticks(np.arange(0, 101, 10))  # Y-axis ticks from 0 to 100 in steps of 10

# Adjust the layout for better spacing
plt.tight_layout()

# Display the plot
plt.show()
