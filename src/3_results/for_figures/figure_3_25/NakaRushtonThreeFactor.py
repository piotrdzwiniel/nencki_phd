import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

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

# Given data
trial_type = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
pulse_duration = np.array([10, 10, 10, 50, 50, 50, 100, 100, 100])
pulse_amplitude = np.array([100, 200, 300, 100, 200, 300, 100, 200, 300])
valid = np.array([0.994851973, 0.760890992, 4.444716001,
                  68.34130879, 91.87515891, 95.08834749,
                  74.89829599, 93.80622773, 96.08315661])


def total_charge(d, A):
    # d in ms, A in µA
    # Convert A (µA to A): A * 1e-6
    # Convert d (ms to s): d * 1e-3
    # Charge (Coulombs) for biphasic pulse: Q = I * t * 2 phases
    Q_coul = (A * 1e-6) * (d * 1e-3) * 2
    # Convert to µC:
    Q_uC = Q_coul * 1e6
    return Q_uC


def naka_rushton_3d(inputs, r_max, sigma_Q, n, sigma_A, m, delta, p, r_base):
    """
    Custom three-dimensional Naka-Rushton model incorporating current pulse total charge, amplitude, and duration to predict response probability/strength.

    Parameters:
    - inputs: tuple (d, A), where:
    d: Pulse duration
    A: Pulse amplitude
    - r_max: Maximum response level (R_max in Naka-Rushton equation)
    - sigma_Q: Half-saturation constant for total charge
    - n: Hill coefficient for total charge
    - sigma_A: Half-saturation constant for amplitude
    - m: Hill coefficient for amplitude
    - delta: Scaling constant for duration effectiveness
    - p: Hill coefficient for duration effectiveness
    - r_base: Baseline response (minimum response level)
    Returns:
    - Predicted response probability
    """

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

initial_guess = [100, 1.0, 1.0, 150.0, 1.0, 10.0, 1.0, 0.0]  # r_max, sigma_Q, n, sigma_A, m, delta, p, r_base

popt, pcov = curve_fit(naka_rushton_3d, xdata=(pulse_duration, pulse_amplitude), ydata=valid,
                       p0=initial_guess, maxfev=20000)

(r_max_fit, sigma_Q_fit, n_fit, sigma_A_fit, m_fit, delta_fit, p_fit, r_base_fit) = popt
print("Fitted parameters:")
print("r_max =", r_max_fit)
print("sigma_Q =", sigma_Q_fit)
print("n =", n_fit)
print("sigma_A =", sigma_A_fit)
print("m =", m_fit)
print("delta =", delta_fit)
print("p =", p_fit)
print("r_base =", r_base_fit)

predictions = naka_rushton_3d((pulse_duration, pulse_amplitude), *popt)
print("Predictions:", predictions)
print("Actual:", valid)

# Goodness of fit (R² equivalent)
Y_pred = predictions
ss_total = np.sum((valid - np.mean(valid)) ** 2)
ss_residual = np.sum((valid - Y_pred) ** 2)
r_squared = 1 - (ss_residual / ss_total)
print(f"Goodness of fit (R²): {r_squared:.4f}")

# Create a grid of duration and amplitude values
d_values = np.linspace(10, 100, 100)  # range from 10 to 100 ms
A_values = np.linspace(100, 300, 100)  # range from 100 to 300 µA

D_grid, A_grid = np.meshgrid(d_values, A_values)

# Predict responses over the grid
Z = naka_rushton_3d((D_grid, A_grid), *popt)

# Make a contour plot
fig, ax = plt.subplots(figsize=(6, 3.5))

plt.rcParams.update({
    'axes.titlesize': 12,   # Title font size
    'axes.labelsize': 12,   # Axis label font size
    'xtick.labelsize': 12,  # X-tick label font size
    'ytick.labelsize': 12   # Y-tick label font size
})

contour = ax.contourf(D_grid, A_grid, Z, levels=20, cmap='viridis')
ax.set_xticks(np.arange(10, 101, 10))


cbar = plt.colorbar(contour, ax=ax)
cbar.set_label('Valid Response Rate (%)', rotation=90)

# Set xtick labels fontsize
for label in ax.get_xticklabels():
    label.set_fontsize(12)
# Set ytick labels fontsize
for label in ax.get_yticklabels():
    label.set_fontsize(12)

# # # Set colorbar ticks
cbar.set_ticks(np.arange(0, 101, 10))

ax.set_xlabel('Pulse Duration (ms)', fontsize=12)
ax.set_ylabel('Pulse Amplitude (µA)', fontsize=12)
ax.set_title('Three-Factor Naka-Rushton Fit (Total Charge, Amplitude, Duration)\nto Valid Response Rate', pad=20, fontsize=12)

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
ax.scatter(pulse_duration, pulse_amplitude, c=valid, cmap='Greys', vmin=0, vmax=100, s=300,
           marker='x')

# Show the plot
plt.tight_layout()
plt.show()
# plt.savefig(f'naka-rushton three-factor fit NEW NEW.png', dpi=300, bbox_inches='tight', transparent=True)
