import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.special import expit
import pandas as pd

# Given data
# trial_type = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
# pulse_duration = np.array([10, 10, 10, 50, 50, 50, 100, 100, 100])
# pulse_amplitude = np.array([100, 200, 300, 100, 200, 300, 100, 200, 300])
# valid = np.array([-0.086, -0.044, 0.07,
#                   0.561, 0.849, 0.976,
#                   0.691, 1.078, 1.022])

# Data setup
data = {
    "trial_type":       [1, 2, 3, 4, 5, 6, 7, 8, 9],
    "pulse_duration":   [10, 10, 10, 50, 50, 50, 100, 100, 100],
    "pulse_amplitude":  [100, 200, 300, 100, 200, 300, 100, 200, 300],
    "valid":            [-0.086, -0.044, 0.07, 0.561, 0.849, 0.976, 0.691, 1.078, 1.022],
}
df = pd.DataFrame(data)

# Prepare the data
X = (df['pulse_duration'], df['pulse_amplitude'])
Y = df['valid']

# Reference LED value as the maximum
LED = 1.269

# Step 1: Shift data to make it non-negative
LED = LED - np.min(Y)
shifted_valid = Y - np.min(Y)

# Step 2: Normalize relative to the LED maximum
Y = (shifted_valid / LED) * 100


def total_charge(d, A):
    """
    Calculate the total charge of a current pulse.

    Parameters:
    - d: Pulse duration in milliseconds (ms).
    - A: Pulse amplitude in microamperes (µA).

    Returns:
    - Total charge in microcoulombs (µC).
    """
    # d in ms, A in µA
    I_pp = A / 1e6  # Peak-to-peak current in amperes (100 µA)
    I_peak = I_pp / 2  # Peak current in amperes
    T_pulse = d / 1e3  # Total pulse duration in seconds (100 ms)
    f = 1 / T_pulse  # Frequency in Hz (assuming full sinusoid fits in pulse duration)

    Q_pulse_analytic_uC = (2 * I_peak) / (np.pi * f) * 1e6
    return Q_pulse_analytic_uC


def naka_rushton_3d(inputs, r_max, sigma_Q, n, sigma_A, m, delta, p, r_base):
    d, A = inputs  # Unpack inputs: pulse duration and amplitude
    Q = total_charge(d, A)  # Calculate total charge per pulse

    # Naka-Rushton equation applied to total charge (Q)
    NR_Q = (Q ** n) / (Q ** n + sigma_Q ** n)

    # Naka-Rushton equation applied to amplitude (A)
    NR_A = (A ** m) / (A ** m + sigma_A ** m)

    # Duration factor: gives higher weight to shorter durations
    # Diminishes as duration (d) increases, based on delta and p
    Dur_factor = (delta ** p) / (delta ** p + d ** p)

    # Combine all factors with baseline response
    return r_base + r_max * NR_Q * NR_A * Dur_factor

"""
Initial guess values:

Index       Value       Parameter       Description
0           100         r_max           Maximum response level, representing the upper bound of the model (asymptote).
1           1.0         sigma_Q         Half-saturation constant for total charge (Q); the charge level at which the response reaches 50% of r_max.
2           1.0         n               Hill coefficient for total charge; controls the steepness of the response curve related to total charge.
3           150.0       sigma_A         Half-saturation constant for pulse amplitude (A); the amplitude level at which the response reaches 50% of r_max.
4           1.0         m               Hill coefficient for amplitude; controls the steepness of the response curve related to amplitude.
5           10.0        delta           Scaling constant for duration effectiveness.
6           1.0         p               Hill coefficient for duration effectiveness; controls how duration influences the response.
7           0.0         r_base          Baseline response (minimum response level); the lowest possible response level when stimulation is minimal.
"""
initial_guess = [100, 1.0, 1.0, 150.0, 1.0, 10.0, 1.0, 0.0]

popt, pcov = curve_fit(naka_rushton_3d, xdata=X, ydata=Y, p0=initial_guess, maxfev=20000)

# popt, pcov = curve_fit(naka_rushton_3d, xdata=(pulse_duration, pulse_amplitude), ydata=valid,
#                        maxfev=20000)

(r_max_fit, sigma_Q_fit, n_fit, sigma_A_fit, m_fit, delta_fit, p_fit, r_base_fit) = popt
print("Fitted parameters:")
print(f"r_max = {r_max_fit:.4f}")
print(f"sigma_Q = {sigma_Q_fit:.4f}")
print(f"n = {n_fit:.4f}")
print(f"sigma_A = {sigma_A_fit:.4f}")
print(f"m = {m_fit:.4f}")
print(f"delta = {delta_fit:.4f}")
print(f"p = {p_fit:.4f}")
print(f"r_base = {r_base_fit:.4f}")

predictions = naka_rushton_3d(X, *popt)

# Goodness of fit (R² equivalent)
Y_pred = predictions
ss_total = np.sum((Y - np.mean(Y)) ** 2)
ss_residual = np.sum((Y - Y_pred) ** 2)
r_squared = 1 - (ss_residual / ss_total)
print(f"Goodness of fit (R²): {r_squared:.4f}")

rounded_Y_pred = np.round(Y_pred.values, 2)
print("Predictions:", rounded_Y_pred)
rounded_Y = np.round(Y.values, 2)
print("Actual:", rounded_Y)

# Calculate percentage difference
diff = Y_pred.values - Y.values
print("Percentage Difference:", np.round(diff, 2))

# Create a grid of duration and amplitude values
d_values = np.linspace(10, 100, 100)  # range from 10 to 100 ms
A_values = np.linspace(100, 300, 100)  # range from 100 to 300 µA

D_grid, A_grid = np.meshgrid(d_values, A_values)

# Predict responses over the grid
Z = naka_rushton_3d((D_grid, A_grid), *popt)

# Make a contour plot
# fig, ax = plt.subplots(figsize=(6, 4.6))
fig, ax = plt.subplots(figsize=(6, 4))

plt.rcParams.update({
    'axes.titlesize': 12,   # Title font size
    'axes.labelsize': 12,   # Axis label font size
    'xtick.labelsize': 12,  # X-tick label font size
    'ytick.labelsize': 12   # Y-tick label font size
})

contour = ax.contourf(D_grid, A_grid, Z, levels=20, cmap='viridis', vmax=100)
ax.set_xticks(np.arange(10, 101, 10))


cbar = plt.colorbar(contour, ax=ax)
cbar.set_label('Percentage of Response\nto Visual Stimulus (%)', rotation=90)

# Set xtick labels fontsize
for label in ax.get_xticklabels():
    label.set_fontsize(12)
# Set ytick labels fontsize
for label in ax.get_yticklabels():
    label.set_fontsize(12)

# # # Set colorbar ticks
# cbar.set_ticks(np.arange(0, 86, 10))
# #
# # # Add minior ticks
# cbar.set_ticklabels(['0', '', '10', '', '20', '', '30', '', '40', '', '50', '',  '60', '',
# '70', '', '80', '', '90', '', '100'])

ax.set_xlabel('Pulse Duration (ms)', fontsize=12)
ax.set_ylabel('Pulse Amplitude (µA)', fontsize=12)
ax.set_title('Three-Factor Naka-Rushton Fit\nto Average P2 Potential', pad=20, fontsize=12)

contour_50 = ax.contour(D_grid, A_grid, Z, levels=[50], colors='black', linestyles='dashed',
                        linewidths=2)
ax.clabel(contour_50, fmt='50%%', inline=True, fontsize=12)

contour_75 = ax.contour(D_grid, A_grid, Z, levels=[75], colors='black',
linestyles='dashed', linewidths=2)
ax.clabel(contour_75, fmt='75%%', inline=True, fontsize=12)

contour_90 = ax.contour(D_grid, A_grid, Z, levels=[90], colors='black', linestyles='dashed',
                        linewidths=2)
ax.clabel(contour_90, fmt='90%%', inline=True, fontsize=12)

ax.scatter(df['pulse_duration'], df['pulse_amplitude'], c=Y, cmap='Greys', vmin=0, vmax=100, s=300,
           marker='x')


###############################################################################################



# Function to extract x-values for specific y-values
def extract_x_for_y(contour, y_values):
    extracted_data = {y: [] for y in y_values}  # Dictionary to store results

    # Iterate through all contour segments (paths)
    for collection in contour.collections:
        for path in collection.get_paths():
            vertices = path.vertices  # Get x, y coordinates of the contour line
            x, y = vertices[:, 0], vertices[:, 1]

            # Check for specific y-values and store corresponding x-values
            for target_y in y_values:
                mask = np.isclose(y, target_y, atol=5)  # Allow small tolerance
                extracted_data[target_y].extend(x[mask])

    return extracted_data


# Define y-values of interest (300 µA, 200 µA, 100 µA)
y_values = [300, 200, 100]

# Extract the x-values corresponding to specific y-values
extracted_x = extract_x_for_y(contour_50, y_values)

# Print results
for y, x_vals in extracted_x.items():
    print(f"50 %% Y = {y} µA -> X-values (Durations): {np.mean(x_vals):.2f} ms")

# # Extract the x-values corresponding to specific y-values
# extracted_x = extract_x_for_y(contour_90, y_values)
#
# # Print results
# for y, x_vals in extracted_x.items():
#     print(f"90 %% Y = {y} µA -> X-values (Durations): {np.mean(x_vals):.2f} ms")


contour_5 = ax.contour(D_grid, A_grid, Z, levels=[10], colors='white', linestyles='dashed',
                        linewidths=2)
ax.clabel(contour_5, fmt='5%%', inline=True, fontsize=12)

# Extract the x-values corresponding to specific y-values
extracted_x = extract_x_for_y(contour_5, y_values)

# Print results
for y, x_vals in extracted_x.items():
    print(f"5 %% Y = {y} µA -> X-values (Durations): {np.mean(x_vals):.2f} ms")
##############################################################################################

plt.tight_layout()
# plt.show()
plt.savefig(f'Corrigenda 3D Naka Rushton EEG.png', dpi=300, bbox_inches='tight', transparent=True)
