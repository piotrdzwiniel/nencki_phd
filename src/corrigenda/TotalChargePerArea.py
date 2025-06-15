import numpy as np

# --- Oblicz total charge per area dla zadanych parametrów ---
def total_charge_one_pulse(duration_s, current_mA):
    """
    Oblicz całkowity ładunek jednego sinusoidalnego impulsu bifazowego (µC).
    """
    duration_ms = duration_s * 1000
    current_uA = current_mA * 1000
    I_pp = current_uA / 1e6  # [A]
    I_peak = I_pp / 2
    T = duration_ms / 1000   # [s]
    f = 1 / T
    Q_pulse = (2 * I_peak) / (np.pi * f) * 1e6  # [µC]
    return Q_pulse

# Przykładowe wartości
current_mA = 0.2        # amplituda
duration_s = 0.1        # czas trwania impulsu
n_pulses = 240          # liczba impulsów
electrode_area = 3      # powierzchnia elektrody (cm²)

# Calculate current density
current_density = current_mA / electrode_area

Q_single = total_charge_one_pulse(duration_s, current_mA)
Q_total = Q_single * n_pulses
Q_per_area = Q_total / electrode_area

# Calculate duration in seconds based on n_pulses and duration_s
total_duration_s = n_pulses * duration_s

# Wyswietl wyniki
print(f"Current density: {current_density:.2f} mA/cm²")
print(f"Total duration: {total_duration_s:.2f} s")
print(f"Total charge for {n_pulses} pulses: {Q_total:.2f} µC")
print(f"Charge per unit area (µC/cm²): {Q_per_area:.2f}")
