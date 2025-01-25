import numpy as np
import matplotlib.pyplot as plt

# Time (in ms)
time = np.linspace(0, 200, 1000)  # Creates a time vector from 0 to 200 ms with 1000 points

# Creating Visual Evoked Potential (VEP)
# Parameters for the components: amplitude, time (in ms), width
n75 = -5 * np.exp(-0.5 * ((time - 75) / 10) ** 2)  # N75 component: negative peak around 75 ms
p100 = 10 * np.exp(-0.5 * ((time - 100) / 10) ** 2)  # P100 component: positive peak around 100 ms
n135 = -7 * np.exp(-0.5 * ((time - 135) / 10) ** 2)  # N135 component: negative peak around 135 ms

# Summing the components to create the full VEP waveform
vep = n75 + p100 + n135

# Plotting the VEP waveform
plt.figure(figsize=(8, 4))  # Set the figure size to 8x4 inches
plt.plot(time, vep, label='VEP', color='blue')  # Plot the VEP waveform
plt.axhline(0, color='black', linewidth=0.5)  # Add a horizontal line at y=0 for reference
plt.axvline(75, color='lightgray', linestyle='--', label='N75')  # Mark the N75 component
plt.axvline(100, color='gray', linestyle='--', label='P100')  # Mark the P100 component
plt.axvline(135, color='darkgray', linestyle='--', label='N135')  # Mark the N135 component

# Adding labels and title to the plot
plt.title('Visual Evoked Potential (VEP)')  # Title of the plot
plt.xlabel('Time (ms)')  # Label for the x-axis
plt.ylabel('Amplitude (µV)')  # Label for the y-axis
plt.legend()  # Display the legend
plt.grid(False)  # Turn off the grid

# Displaying the plot
plt.show()  # Show the plot
