import mne
import matplotlib.pyplot as plt
import numpy as np

epochs = mne.read_epochs('../../data/ledes/all-cleaned-occipital-epo.fif')

event_dict = {
        "pCS 10 ms 100 µA": 1,
        "pCS 10 ms 200 µA": 2,
        "pCS 10 ms 300 µA": 3,
        "pCS 50 ms 100 µA": 4,
        "pCS 50 ms 200 µA": 5,
        "pCS 50 ms 300 µA": 6,
        "pCS 100 ms 100 µA": 7,
        "pCS 100 ms 200 µA": 8,
        "pCS 100 ms 300 µA": 9,
        "100 ms LED Flash": 10
    }

# Choose
epochs_1 = epochs['pCS 10 ms 100 µA'].get_data()*1e6
epochs_2 = epochs['pCS 10 ms 200 µA'].get_data()*1e6
epochs_3 = epochs['pCS 10 ms 300 µA'].get_data()*1e6
epochs_4 = epochs['pCS 50 ms 100 µA'].get_data()*1e6
epochs_5 = epochs['pCS 50 ms 200 µA'].get_data()*1e6
epochs_6 = epochs['pCS 50 ms 300 µA'].get_data()*1e6
epochs_7 = epochs['pCS 100 ms 100 µA'].get_data()*1e6
epochs_8 = epochs['pCS 100 ms 200 µA'].get_data()*1e6
epochs_9 = epochs['pCS 100 ms 300 µA'].get_data()*1e6
epochs_10 = epochs['100 ms LED Flash'].get_data()*1e6

cond_label = "100 ms LED Flash"
data = epochs_10

# Get n_epochs
n_epochs = data.shape[0]

# Step 1: Average across epochs
mean_data = np.mean(data, axis=0)  # Shape: (channels, samples)

# Step 2: Calculate GFP (standard deviation across channels at each time point)
gfp = np.std(mean_data, axis=0)  # Shape: (samples,)

# Generate time axis
times = np.linspace(-0.5, 1.0, len(gfp))  # From -0.5 to 1.0 seconds

# Ustalanie przedziału bazowego (od -0.5 do 0 s)
baseline_start = -0.2
baseline_end = 0.0

# Indeksy odpowiadające przedziałowi bazowemu
baseline_indices = (times >= baseline_start) & (times < baseline_end)

# Oblicz średnią w oknie bazowym (dla każdego kanału i epoki, jeśli dane mają więcej wymiarów)
baseline_mean = np.mean(gfp[baseline_indices])

gfp = gfp - baseline_mean

# Step 3: Plotting GFP with shaded area under the curve
plt.rcParams.update({'font.size': 11})
fig, ax = plt.subplots(figsize=(4.5, 2))
ax.plot(times, gfp, color='black', label='GFP', linewidth=2)  # Plot GFP
ax.fill_between(times, 0, gfp, color='lightgray', alpha=1)  # Fill under the curve (from 0 to GFP)

plt.axvline(x=0, color='black', linestyle='--', linewidth=1.0)

# Formatting the plot
ax.set_xlim([-0.1, 0.7])  # Set x-axis limits
ax.set_xticks(np.arange(-0.1, 0.8, 0.1))
ax.set_ylim([0, 1.1])
ax.set_yticks(np.arange(0, 1.1, 0.5))
ax.set_xlabel('Time (s)', fontsize=12)
ax.set_ylabel('GFP (µV)', fontsize=12)
ax.set_title('Global Field Power (GFP)\nfor Occipital Channels', fontsize=12)

# Display the plot
plt.tight_layout()
plt.show()

# Save
# plt.savefig(f'GFP {cond_label}.png', dpi=300, bbox_inches='tight', transparent=True)
