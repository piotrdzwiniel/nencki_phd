import pandas as pd
import ptitprince as pt
import matplotlib.pyplot as plt
import numpy as np

# Load the data from the provided CSV file
file_path = '../../data/ledes/all_subjects_responses_and_times.csv'
data = pd.read_csv(file_path)

# Exclude subject 'PA_11042022_M'
data = data[data['subject'] != 'PA_11042022_M']

y_data = 'mean'
sems = 'sem'

# Exclude negative values
data = data[data[y_data] >= 0]

# Group trial types
groups = [
    [0],  # First plot
    [3],  # Second plot
    [4, 5, 6],  # Third plot
    [7, 8, 9]  # Fourth plot
]

labels = [
    ['LED'],  # First plot
    ['300 µA'],  # Second plot
    ['100 µA', '200 µA', '300 µA'],  # Third plot
    ['100 µA', '200 µA', '300 µA']  # Fourth plot
]

# Titles for subplots
titles = ["100 ms Light", "10 ms pCS", "50 ms pCS", "100 ms pCS"]

# Colors for bars
colors = ['lightgray', 'darkgray', 'dimgray']

# Create figure with specified width ratios
fig, axes = plt.subplots(1, 4, figsize=(10, 3),
                         gridspec_kw={'width_ratios': [1, 1, 3, 3]}, sharey=True)

# Fontsize rc params
plt.rcParams.update({'font.size': 11})
# padding=0.2

# Iterate over the grouped trial types and plot data
led_mean_ms = None
for i, (ax, trials, label) in enumerate(zip(axes, groups, labels)):
    # Filter data for the current group
    group_data = data[data['trial_type'].isin(trials)]

    # Calculate mean and SEM
    mean_values = group_data.groupby('trial_type')[y_data].mean()
    sem_values = group_data.groupby('trial_type')[y_data].sem()


    color = None
    if 0 in trials:
        color = 'darkorange'
    elif 3 in trials:
        color = colors[0]
    elif 4 in trials:
        color = colors[1]
    elif 7 in trials:
        color = colors[2]

    a = pt.half_violinplot(data=group_data, x='trial_type', y=y_data, palette=[color], ax=ax,
                           width=0.75, bw=0.75, linewidth=2, inner='box', offset=0.4,
                           saturation=1)

    for violin in a.collections:
        violin.set_edgecolor('black')

    for line in a.lines:
        line.set_color('black')

    for j, group in enumerate(trials):
        # Subset the data
        temp_data = data[data["trial_type"] == group]

        # Jitter the values on the vertical axis
        x = j + np.random.uniform(high=0.025, size=len(temp_data)) - 0.25  # - 0.175

        # Select the values of the horizontal axis
        y = temp_data[y_data]

        # Add the rain using the scatter method
        ax.scatter(x, y, color=color, alpha=0.5)

    # Set titles and x-axis labels
    ax.set_title(titles[i], fontsize=12, pad=20)
    ax.set_xticklabels(label, rotation=45, ha='right', fontsize=11)

    if 0 in trials or 3 in trials:
        ax.margins(x=0.15)

    if 0 not in trials:
        # Set hline
        ax.axhline(led_mean_ms, color='black', linestyle='--', linewidth=1, label='LED Mean')
        if 9 in trials:
            # Legend
            ax.legend(loc='upper right', fontsize=11)
    else:
        led_mean_ms = mean_values.values[0]
        ax.axhline(led_mean_ms, color='black', linestyle='--', linewidth=1, label='LED Mean')

    ax.set_ylabel("", fontsize=12)
    ax.set_xlabel("", fontsize=12)

# Set the common y-axis label
axes[0].set_ylabel("Response Time (ms)", fontsize=12)
axes[0].set_ylim(0, 1000)
axes[0].set_yticks(np.arange(0, 1001, 200))
axes[0].set_yticklabels(np.arange(0, 1001, 200), fontsize=11)

# Ensure tight layout
plt.tight_layout()

# Show the plot
plt.show()

# Save
# plt.savefig(f'RPFigure_B_Distros_AXIS.png', dpi=300, bbox_inches='tight', transparent=True)
