import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import pandas as pd

"""
Data dictionary (dict: data) for the Naka-Rushton Single Factor Model.

Fields:
- trial_type: Identifier for trial types, corresponding to specific current pulse parameters.
- pulse_duration: Pulse duration in milliseconds (ms).
- pulse_amplitude: Pulse amplitude in milliamperes (mA).
- valid: Valid response rate, representing the detection rate of visual stimuli and phosphenes induced by pulses.

Trial Type Definitions (pulse duration in ms, pulse amplitude in mA):
1  →  10ms, 100mA  
2  →  10ms, 200mA  
3  →  10ms, 300mA  
4  →  50ms, 100mA  
5  →  50ms, 200mA  
6  →  50ms, 300mA  
7  →  100ms, 100mA  
8  →  100ms, 200mA  
9  →  100ms, 300mA  
"""

# Data setup
data = {
    "trial_type":       [1, 2, 3, 4, 5, 6, 7, 8, 9],
    "pulse_duration":   [10, 10, 10, 50, 50, 50, 100, 100, 100],
    "pulse_amplitude":  [100, 200, 300, 100, 200, 300, 100, 200, 300],
    "valid":            [0.994851973, 0.760890992, 4.444716001, 68.34130879, 91.87515891,
                         95.08834749, 74.89829599, 93.80622773, 96.08315661],
}
df = pd.DataFrame(data)


# Naka-Rushton function (single-factor model) using total charge to model nonlinear responses
def naka_rushton(inputs, r_max, sigma, n, r_base):
    """
    Computes the response based on the Naka-Rushton equation, which models the relationship
    between stimulus intensity and neural response with a saturating nonlinearity.

    Parameters:
    - inputs (tuple): A tuple containing (pulse_duration in ms, pulse_amplitude in mA).
    - r_max (float): Maximum response value.
    - sigma (float): Semi-saturation constant (stimulus intensity at half-max response).
    - n (float): Exponent controlling the steepness of the response curve.
    - r_base (float): Baseline response.

    Returns:
    - float: The computed response value.
    """

    duration, amplitude = inputs  # Unpack input values

    # Compute peak current (mA) assuming a biphasic waveform
    I_peak = amplitude / 2

    # Compute half the pulse duration (ms)
    t_half_phase = duration / 2

    # Compute RMS (Root Mean Square) current
    I_RMS = I_peak / np.sqrt(2)

    # Calculate charge per phase (Coulombs)
    charge_per_phase = I_RMS * t_half_phase  # Charge = I_RMS * t_half_phase

    # Compute total charge per pulse (sum of both phases, in microCoulombs)
    charge_per_pulse = 2 * charge_per_phase

    # Use charge per pulse as the stimulus intensity for the Naka-Rushton function
    stim = charge_per_pulse

    # Compute the Naka-Rushton response
    response = r_max * (stim ** n) / (stim ** n + sigma ** n) + r_base
    return response

# Prepare the data
X = (df['pulse_duration'], df['pulse_amplitude'])
Y = df['valid']

# Provide initial guesses for the parameters
initial_guesses = [100, 100, 1, 0]  # R_max, sigma, n, r_base

# Perform the curve fitting
popt, pcov = curve_fit(
    naka_rushton,
    X,
    Y,
    bounds=(0, np.inf),  # Ensure parameters stay non-negative
    p0=initial_guesses,
    maxfev=20000  # Increase maxfev to allow more iterations
)

# Extract fitted parameters
r_max, sigma, n, r_base = popt
print("Fitting parameters:")
print(f"R_max (maximum response): {r_max}")
print(f"Sigma (semi-saturation constant): {sigma}")
print(f"n (steepness exponent): {n}")
print(f"R_base (baseline response): {r_base}")

# Goodness of fit (R² equivalent)
Y_pred = naka_rushton(X, *popt)
ss_total = np.sum((Y - np.mean(Y)) ** 2)
ss_residual = np.sum((Y - Y_pred) ** 2)
r_squared = 1 - (ss_residual / ss_total)
print(f"Goodness of fit (R²): {r_squared:.4f}")

print("Predictions:", Y_pred)
print("Actual:", Y.values)

# Create a grid of duration and amplitude values
d_values = np.linspace(10, 100, 100)  # range from 10 to 100 ms
A_values = np.linspace(100, 300, 100)  # range from 100 to 300 µA

D_grid, A_grid = np.meshgrid(d_values, A_values)

# Predict responses over the grid
Z = naka_rushton((D_grid, A_grid), *popt)

# Make a contour plot
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

ax.set_xlabel('Pulse Duration (ms)', fontsize=12)
ax.set_ylabel('Pulse Amplitude (µA)', fontsize=12)
ax.set_title('Single-Factor Naka-Rushton Fit (Total Charge)\nto Valid Response Rate', pad=20, fontsize=12)

contour_90 = ax.contour(D_grid, A_grid, Z, levels=[90], colors='black', linestyles='dashed', linewidths=2)
ax.clabel(contour_90, fmt='90%%', inline=True, fontsize=12)

contour_50 = ax.contour(D_grid, A_grid, Z, levels=[50], colors='black', linestyles='dashed', linewidths=2)
ax.clabel(contour_50, fmt='50%%', inline=True, fontsize=12)

contour_5 = ax.contour(D_grid, A_grid, Z, levels=[5], colors='white', linestyles='dashed', linewidths=2)
ax.clabel(contour_5, fmt='5%%', inline=True, fontsize=12)

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

# Extract the x-values corresponding to specific y-values
extracted_x = extract_x_for_y(contour_90, y_values)

# Print results
for y, x_vals in extracted_x.items():
    print(f"90 %% Y = {y} µA -> X-values (Durations): {np.mean(x_vals):.2f} ms")

# Extract the x-values corresponding to specific y-values
extracted_x = extract_x_for_y(contour_5, y_values)

# Print results
for y, x_vals in extracted_x.items():
    print(f"5 %% Y = {y} µA -> X-values (Durations): {np.mean(x_vals):.2f} ms")

# Scatter plot of the data points
ax.scatter(df['pulse_duration'], df['pulse_amplitude'], c=df['valid'], cmap='Greys', vmin=0, vmax=100, s=300,
           marker='x')

# Show the plot
plt.tight_layout()
plt.show()
# plt.savefig(f'naka-rushton single-factor fit NEW.png', dpi=300, bbox_inches='tight', transparent=True)
