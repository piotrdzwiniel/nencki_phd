import numpy as np
import matplotlib.pyplot as plt
import Utils as ut

# Set global font size for all plots
plt.rcParams.update({'font.size': 11})

# Define parameters for pulse generation (duration in ms, amplitude in µA)
params = [
    (100, 100),  # 100 ms, 100 µA
    (50, 100),   # 50 ms, 100 µA
    (25, 100),   # 25 ms, 100 µA
    (12.5, 100), # 12.5 ms, 100 µA
    (100, 200),  # 100 ms, 200 µA
    (50, 200),   # 50 ms, 200 µA
    (25, 200),   # 25 ms, 200 µA
    (12.5, 200), # 12.5 ms, 200 µA
    (100, 300),  # Control (no pulse)
    (1, 1),      # Placeholder
    (1, 1),      # Placeholder
    (1, 1)       # Placeholder
]

# Create a time scale using utility function (assumed 100 samples, 1000 Hz sampling rate)
timescale = ut.create_time_scale(100, 1000, 'ms')

# Create subplots with shared X and Y axes
fig, axs = plt.subplots(3, 4, figsize=(7, 5), sharey=True, sharex=True)  # 3 rows, 4 columns

for i, (ax, (duration, amplitude)) in enumerate(zip(axs.flat, params)):
    if i < 9:  # Only fill the first 9 subplots with data
        pulse, _ = ut.create_sin_pulse(1000.0 / duration, 1000, float(amplitude))  # Generate sinusoidal pulse

        # Pad pulse with zeros to make its length equal to 100
        pulse = np.pad(pulse, (0, 100 - len(pulse)), 'constant', constant_values=0)

        # Set the pulse to zero if it matches the control condition (100 ms, 300 µA)
        if duration == 100 and amplitude == 300:
            pulse[:] = 0

        # Plot the pulse signal
        ax.plot(timescale, pulse, color='black', linewidth=1.75)
        # ax.set_title(f'{int(duration)} ms {int(amplitude)} µA')  # Optionally set the title
        ax.set_ylim(-115, 115)  # Set Y-axis limits
        ax.set_xlim(-10, 110)   # Set X-axis limits

        # Add ticks on the axes at intervals of 50 units
        ax.set_xticks(np.arange(0, 106, 50))  # X-axis ticks
        ax.set_yticks(np.arange(-100, 101, 50))  # Y-axis ticks

        # Set X-axis label only for the control plot (100 ms, 300 µA)
        if duration == 100 and amplitude == 300:
            ax.set_xlabel('Time (ms)')

        # Set Y-axis label only for the specified subplot (for better labeling clarity)
        if i == 4:
            ax.set_ylabel('Amplitude (µA)')
    else:
        # Remove unused axes (placeholders)
        fig.delaxes(ax)

plt.tight_layout()  # Adjust layout to prevent overlapping elements
# Optionally save the plot as an image
# plt.savefig('pCS_Pulses_IMP.png', dpi=300, bbox_inches='tight', transparent=True)
plt.show()
