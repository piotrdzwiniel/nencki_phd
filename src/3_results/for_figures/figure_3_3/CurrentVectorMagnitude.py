import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Given data
data = {
    "Time (s)": [0.000, 0.005, 0.010, 0.015, 0.020, 0.025, 0.030, 0.035, 0.040, 0.045, 0.050,
                 0.055, 0.060, 0.065, 0.070, 0.075, 0.080, 0.085, 0.090, 0.095, 0.100],
    "Electrode A (µA)": [0.00, 15.45, 29.39, 40.45, 47.55, 50.00, 47.55, 40.45, 29.39, 15.45,
                         0.00, -15.45, -29.39, -40.45, -47.55, -50.00, -47.55, -40.45, -29.39,
                         -15.45, 0.00],
    "Electrode B (µA)": [0.00, -15.45, -29.39, -40.45, -47.55, -50.00, -47.55, -40.45, -29.39,
                         -15.45, 0.00, 15.45, 29.39, 40.45, 47.55, 50.00, 47.55, 40.45, 29.39,
                         15.45, 0.00]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Convert time to milliseconds
df["Time (ms)"] = df["Time (s)"] * 1000

# Calculate the vector magnitude using the absolute difference between Electrode A and Electrode B
df["Vector Magnitude (µA)"] = np.abs(df["Electrode A (µA)"] - df["Electrode B (µA)"])

# Calculate the vector direction (angle in degrees)
# df["Vector Direction (degrees)"] = np.degrees(np.arctan2(df["Electrode B (µA)"], df["Electrode A (µA)"]))

# Calculate the vector direction (angle in degrees) only for non-zero values
non_zero_mask = (df["Electrode A (µA)"] != 0) | (df["Electrode B (µA)"] != 0)
df["Vector Direction (degrees)"] = np.nan  # Initialize with NaN for all rows
df.loc[non_zero_mask, "Vector Direction (degrees)"] = np.degrees(
    np.arctan2(df.loc[non_zero_mask, "Electrode B (µA)"], df.loc[non_zero_mask, "Electrode A (µA)"])
)


# Create subplots
fig, axs = plt.subplots(1, 2, figsize=(12, 4), gridspec_kw={'width_ratios': [2, 1], 'height_ratios': [1]})

# Plotting the vector magnitude over time on the left (2/3 space)
axs[0].plot(df["Time (ms)"], df["Vector Magnitude (µA)"], marker='o', markersize=8,
            label="Vector Magnitude (µA)", color='darkslategray', alpha=0.25, linestyle='--')
axs[0].set_xlabel("Time (ms)", fontsize=12)
axs[0].set_ylabel("Vector Magnitude (µA)", fontsize=12)
axs[0].set_title("Current Vector Magnitude (Absolute Difference) Over Time", fontsize=14, pad=30)
axs[0].grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
axs[0].set_xticks(np.arange(0, 110, 10))
axs[0].set_yticks(np.arange(0, 101, 10))  # Setting y-axis ticks from 0 to 100 with a step of 10
axs[0].tick_params(axis='both', which='major', labelsize=12)

# Add arrows for all points, size depending on the magnitude
for i in range(len(df)):
    magnitude = df["Vector Magnitude (µA)"][i]
    color = '#FF2600' if df["Time (ms)"][i] >= 50 else '#4181FF'
    arrowprops = dict(facecolor=color, edgecolor='black', shrink=0.05, width=1.5, headwidth=10,
                      headlength=10, alpha=1)
    if df["Time (ms)"][i] >= 50:
        axs[0].annotate('',
                        xy=(df["Time (ms)"][i], df["Vector Magnitude (µA)"][i] + magnitude / 10),
                        xytext=(df["Time (ms)"][i], df["Vector Magnitude (µA)"][i] - magnitude / 10),
                        arrowprops=arrowprops)
    else:
        axs[0].annotate('',
                        xy=(df["Time (ms)"][i], df["Vector Magnitude (µA)"][i] - magnitude / 10),
                        xytext=(df["Time (ms)"][i], df["Vector Magnitude (µA)"][i] + magnitude / 10),
                        arrowprops=arrowprops)

axs[0].set_ylim(-10, 110)

# Polar plot on the right (1/3 space) showing the vector direction over time
axs[1] = plt.subplot(122, polar=True)
angles = np.radians(df["Vector Direction (degrees)"])
magnitude = df["Vector Magnitude (µA)"]
colors = ['#FF2600' if t >= 50 else '#4181FF' for t in df["Time (ms)"]]
sc = axs[1].scatter(angles, magnitude, c=colors, cmap='coolwarm', alpha=1, edgecolor='black', s=50)
axs[1].set_title("Vector Direction Over Time", fontsize=14, pad=10)
axs[1].set_theta_zero_location('E')  # 0 degrees at the right (East)
axs[1].set_theta_direction(-1)  # Clockwise direction
axs[1].set_xticks([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi, 5*np.pi/4, 3*np.pi/2, 7*np.pi/4])  # 0, 45, 90, ..., 315 degrees
axs[1].set_xticklabels(['0°', '45°', '90°', '135°', '180°', '225°', '270°', '315°'], fontsize=12)
axs[1].set_yticks([25, 50, 75, 100])  # Setting radial ticks to 25, 50, 75, and 100 µA
axs[1].grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

plt.tight_layout()
plt.show()
# plt.savefig('vector_magnitude_and_direction.png', dpi=300, bbox_inches='tight', transparent=True)
