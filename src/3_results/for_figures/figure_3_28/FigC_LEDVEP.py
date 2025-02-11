import mne
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import sem

# Load preprocessed EEG epochs
epochs = mne.read_epochs('../../data/ledes/all-cleaned-occipital-epo.fif')

# Select condition data (convert to microvolts)
cond_label = "100 ms LED Flash"
condition = epochs['100 ms LED Flash'].get_data() * 1e6  # Convert to µV

# Compute the mean response across epochs and channels
vector = np.mean(condition, axis=(0, 1))  # Average over epochs and channels

# Compute the standard error of the mean (SEM) across epochs
sem_vector = sem(condition, axis=0)  # Compute SEM across epochs
sem_vector = np.mean(sem_vector, axis=0)  # Average SEM across channels

# Generate time vector from -0.5 to 1.0 seconds
time_vector = np.linspace(-0.5, 1.0, len(vector))

# Define the baseline period (e.g., from -0.2 to 0.0 s)
baseline_start = -0.2
baseline_end = 0.0

# Identify indices corresponding to the baseline window
baseline_indices = (time_vector >= baseline_start) & (time_vector < baseline_end)

# Compute the baseline mean and subtract it from the data
baseline_mean = np.mean(vector[baseline_indices])
vector = vector - baseline_mean  # Baseline correction

# Configure plot settings
plt.rcParams.update({'font.size': 11})
plt.figure(figsize=(4.5, 3))  # Adjust figure size

# Highlight the stimulus presentation window
plt.axvspan(0, 0.1, facecolor='darkorange', alpha=0.2, label=f"{cond_label}")

# Add horizontal and vertical reference lines
plt.axhline(y=0, color='black', linewidth=0.8)
plt.axvline(x=0, color='black', linestyle='--', linewidth=1.0)

# Plot the event-related potential (ERP) signal
plt.plot(time_vector, vector, color='black', linewidth=1.5)

# Add shaded area representing the SEM
plt.fill_between(time_vector, vector - sem_vector, vector + sem_vector, color='gray', alpha=0.4)

# Set x-axis limits and ticks
plt.xlim(-0.1, 0.7)  # Define time window
plt.xticks(np.arange(-0.1, 0.71, 0.1))  # Set tick marks every 0.1s

# Set y-axis limits
plt.ylim(-6, 6)  # Adjust y-range based on the signal amplitude

# Add axis labels and title
plt.title('Occipital VEP', fontsize=12)
plt.xlabel('Time (s)', fontsize=12)
plt.ylabel('Amplitude (µV)', fontsize=12)

# Add legend
plt.legend(loc='upper right', fontsize=11)

# Optimize layout and display plot
plt.tight_layout()
plt.show()
