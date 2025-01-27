import numpy as np
import matplotlib.pyplot as plt
import Utils as ut

# Set global font size for plots
plt.rcParams.update({'font.size': 10})

# Parameter settings for the pulses (duration in ms, amplitude in µA)
params = [
    (10, 100),  # Pulse: 10 ms duration, 100 µA amplitude
    (10, 200),  # Pulse: 10 ms duration, 200 µA amplitude
    (10, 300),  # Pulse: 10 ms duration, 300 µA amplitude
    (50, 100),  # Pulse: 50 ms duration, 100 µA amplitude
    (50, 200),  # Pulse: 50 ms duration, 200 µA amplitude
    (50, 300),  # Pulse: 50 ms duration, 300 µA amplitude
    (100, 100),  # Pulse: 100 ms duration, 100 µA amplitude
    (100, 200),  # Pulse: 100 ms duration, 200 µA amplitude
    (100, 300)   # Pulse: 100 ms duration, 300 µA amplitude
]

# Generate a timescale for plotting (100 points, 1000 Hz sampling rate, time unit in milliseconds)
timescale = ut.create_time_scale(100, 1000, 'ms')

# Create a figure with 1 row and 9 columns, sharing the Y-axis across all subplots
fig, axs = plt.subplots(1, 9, figsize=(10, 1.75), sharey=True)  # 1 row, 9 columns

# Iterate over each subplot and parameter set (duration, amplitude)
for i, (ax, (duration, amplitude)) in enumerate(zip(axs, params)):
    # Generate a sinusoidal pulse based on the given duration and amplitude
    pulse, _ = ut.create_sin_pulse(1000 / duration, 1000, amplitude)

    # Pad the pulse with zeros to make its length equal to 100
    pulse = np.pad(pulse, (0, 100 - len(pulse)), 'constant', constant_values=0)

    # Plot the pulse
    ax.plot(timescale, pulse, color='black')
    # Optional: set the title for each subplot (commented out)
    # ax.set_title(f'{int(duration)} ms {int(amplitude)} µA')

    # Set the Y-axis range for all plots
    ax.set_ylim(-165, 165)
    # Set the X-axis range for all plots
    ax.set_xlim(-10, 110)

    # Add ticks on the X-axis at intervals of 50 units
    ax.set_xticks(np.arange(0, 106, 50))
    # Add ticks on the Y-axis at intervals of 50 units
    ax.set_yticks(np.arange(-150, 151, 50))

    # Set the X-axis label only for the plot with a 50 ms, 200 µA pulse
    if duration == 50 and amplitude == 200:
        ax.set_xlabel('Time (ms)')

    # Set the Y-axis label only for the first plot
    if i == 0:
        ax.set_ylabel('Amplitude (µA)')

# Adjust the layout to avoid overlapping elements
plt.tight_layout()
# Save the plot as a PNG file with high resolution and transparency
# plt.savefig('pCS_Pulses_LEDES_TEST.png', dpi=300, bbox_inches='tight', transparent=True)
# Display the plot
plt.show()
