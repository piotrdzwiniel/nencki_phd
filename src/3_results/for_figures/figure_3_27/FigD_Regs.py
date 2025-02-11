import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

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
fig, axes = plt.subplots(1, 2, figsize=(5, 3), gridspec_kw={'width_ratios': [1, 1]}, sharey=True)

# Second subplot: 50 ms with linear regression
ax2 = axes[0]
X_456 = np.array([100, 200, 300]).reshape(-1, 1)  # Reshape for sklearn
y_456 = mean_456.values

# Linear regression
model_50ms = LinearRegression().fit(X_456, y_456)
y_pred_50ms = model_50ms.predict(X_456)

# Plot data points and regression line
ax2.scatter([100, 200, 300], y_456, color='darkgray', edgecolor='k', s=75)
ax2.plot([100, 200, 300], y_pred_50ms, color='darkgray', linestyle='--', label=f'R² = {model_50ms.score(X_456, y_456):.2f}', zorder=3)
ax2.legend(fontsize=11, loc='upper center', bbox_to_anchor=(0.5, 1.0175))

# Customize
ax2.set_title("50 ms pCS", fontsize=12, pad=20)
ax2.set_ylabel("Response Time (ms)", fontsize=12)
ax2.set_xlabel("Amplitude (µA)", fontsize=12)
ax2.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.7)
ax2.set_ylim(300, 550)

# Third subplot: 100 ms with linear regression
ax3 = axes[1]
X_789 = np.array([100, 200, 300]).reshape(-1, 1)  # Reshape for sklearn
y_789 = mean_789.values

# Linear regression
model_100ms = LinearRegression().fit(X_789, y_789)
y_pred_100ms = model_100ms.predict(X_789)

# Display regression results
print(f"50 ms pCS: Intercept = {model_50ms.intercept_:.2f}, Slope = {model_50ms.coef_[0]:.2f}")
print(f"50 ms pCS: R^2 = {model_50ms.score(X_456, y_456):.2f}")
print()
print(f"100 ms pCS: Intercept = {model_100ms.intercept_:.2f}, Slope = {model_100ms.coef_[0]:.2f}")
print(f"100 ms pCS: R^2 = {model_100ms.score(X_789, y_789):.2f}")

# Plot data points and regression line
ax3.plot([100, 200, 300], y_pred_100ms, color='dimgray', linestyle='--', label=f'R² = {model_100ms.score(X_789, y_789):.2f}', zorder=3)
ax3.scatter([100, 200, 300], y_789, color='dimgray', edgecolor='k', s=75)
ax3.legend(fontsize=11, loc='upper center', bbox_to_anchor=(0.5, 1.0175))

# Customize
ax3.set_title("100 ms pCS", fontsize=12, pad=20)
ax3.set_xlabel("Amplitude (µA)", fontsize=12)
ax3.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.7)
ax3.set_ylim(300, 550)

# Final layout
plt.tight_layout()
plt.show()

# Save
# plt.savefig(f' 50 and 100 ms linear regressions.png', dpi=300, bbox_inches='tight', transparent=True)
