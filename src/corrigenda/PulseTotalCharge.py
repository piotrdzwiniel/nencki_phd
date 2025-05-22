import numpy as np
from scipy.integrate import quad

# List of pulses defined by their durations (ms) and amplitudes (µA peak-to-peak)
pulses = [
    {"duration": 10, "amplitude": 100},
    {"duration": 10, "amplitude": 200},
    {"duration": 10, "amplitude": 300},
    {"duration": 50, "amplitude": 100},
    {"duration": 50, "amplitude": 200},
    {"duration": 50, "amplitude": 300},
    {"duration": 100, "amplitude": 100},
    {"duration": 100, "amplitude": 200},
    {"duration": 100, "amplitude": 300}
]

# Iterate over pulse definitions and compute total charge per pulse
for pulse in pulses:
    duration = pulse["duration"]      # duration in milliseconds
    amplitude = pulse["amplitude"]    # peak-to-peak current in microamperes

    print(f"Duration: {duration} ms, Amplitude: {amplitude} µA")

    # Convert amplitude to amperes
    I_pp = amplitude / 1e6            # peak-to-peak current in amperes
    I_peak = I_pp / 2                 # peak current in amperes

    # Convert duration to seconds and compute frequency
    T = duration / 1e3                # total pulse duration in seconds
    f = 1 / T                         # frequency in Hz

    # === EXTENDED METHOD (using integration) ===
    # Define sinusoidal current function for one half-phase
    I_t = lambda t: I_peak * np.sin(2 * np.pi * f * t)

    # Integrate current over one half-phase (from 0 to T/2)
    Q_half, _ = quad(I_t, 0, T / 2)

    # Multiply by 2 for the full biphasic pulse
    Q_total = 2 * Q_half

    # Convert total charge to microcoulombs (µC)
    Q_microC = Q_total * 1e6

    print(f"Total charge per pulse (integral method): {Q_microC:.4f} µC")

    # === SIMPLIFIED METHOD (closed-form expression) ===
    Q_pulse = (2 * I_peak) / (np.pi * f) * 1e6  # in microcoulombs

    print(f"Total charge per pulse (analytical method): {Q_pulse:.4f} µC\n")
