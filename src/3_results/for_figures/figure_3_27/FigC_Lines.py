import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the provided CSV file
file_path = '../../data/ledes/all_subjects_responses_and_times.csv'
data = pd.read_csv(file_path)

y_data = 'mean'
sems = 'sem'

# Exclude subject 'PA_11042022_M'
data = data[data['subject'] != 'PA_11042022_M']

# Exclude negative values
data = data[data[y_data] >= 0]

# Group trial types
trial_types = [
    [0],  # First mean horizontal line
    [3],  # Second mean horizontal line
    [4, 5, 6],  # First line plot with sems
    [7, 8, 9]  # Second line plot with sems
]

# Group trial types
trial_types = {
    "horizontal_0": [0],  # First mean horizontal line
    "horizontal_3": [3],  # Second mean horizontal line
    "line_456": [4, 5, 6],  # First line plot with SEMs
    "line_789": [7, 8, 9]  # Second line plot with SEMs
}

mean_0 = data[data['trial_type'] == 0][y_data].mean()
mean_3 = data[data['trial_type'] == 3][y_data].mean()

data_456 = data[data['trial_type'].isin([4, 5, 6])]
mean_456 = data_456.groupby('trial_type')[y_data].mean()
sem_456 = data_456.groupby('trial_type')[y_data].sem()

data_789 = data[data['trial_type'].isin([7, 8, 9])]
mean_789 = data_789.groupby('trial_type')[y_data].mean()
sem_789 = data_789.groupby('trial_type')[y_data].sem()

# Tick rc params
plt.rcParams.update({'font.size': 11})
plt.rcParams.update({'xtick.labelsize': 11})
plt.rcParams.update({'ytick.labelsize': 11})

# Create the figure with width ratios
fig, axes = plt.subplots(1, 1, figsize=(5, 3))

# First subplot: Combined plot
ax1 = axes

# Add horizontal lines
ax1.axhline(mean_0, color='darkorange', linestyle='--', linewidth=1.5, label="100 ms LED Flash")
ax1.axhline(mean_3, color='lightgray', linestyle='--', linewidth=1.5, label="10 ms 300 µA pCS")

# Add 50 ms line
ax1.errorbar([100, 200, 300], mean_456, yerr=sem_456, fmt='o-', label="50 ms pCS", color='darkgray', capsize=5)

# Add 100 ms line
ax1.errorbar([100, 200, 300], mean_789, yerr=sem_789, fmt='o-', label="100 ms pCS", color='dimgray', capsize=5)

# Customize
ax1.set_title("50 ms vs. 100 ms pCS", fontsize=12, pad=20)
ax1.set_xlabel("Amplitude (µA)", fontsize=12)
ax1.set_ylabel("Response Time (ms)", fontsize=12)
ax1.set_xticks([100, 200, 300])
ax1.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.7)
ax1.set_ylim(300, 550)

# Shrink current axis by 20%
box = ax1.get_position()
ax1.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=11)

plt.subplots_adjust(right=0.15)
plt.tight_layout()
plt.show()

# Save
# plt.savefig(f' 50 vs 100 ms pCS.png', dpi=300, bbox_inches='tight', transparent=True)
