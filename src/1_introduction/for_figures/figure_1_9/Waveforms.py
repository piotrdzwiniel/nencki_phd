import numpy as np
import matplotlib.pyplot as plt
import Utils as ute

# Generate a time vector from 0 to 4π with 1000 points
t = np.linspace(0, 4 * np.pi, 1000)

# Define zero padding for periods before and after stimulation
zero_padding = np.zeros(50)

# 1. Transcranial Direct Current Stimulation (tDCS) - Constant DC offset
# Create a constant signal with an offset of 0.5, padded with zeros
tdcs_signal = np.concatenate((zero_padding, np.ones_like(t) * 0.5, zero_padding))

# 2. Transcranial Alternating Current Stimulation (tACS) - Sinusoidal waveform
# Create a sinusoidal signal with a frequency of 5 and amplitude of 0.5, padded with zeros
tacs_signal = np.concatenate((zero_padding, 0.5 * np.sin(5 * t), zero_padding))

# 3. Transcranial Random Noise Stimulation (tRNS) - Random noise
# Generate random noise with mean 0 and standard deviation 0.2, padded with zeros
trns_signal = np.concatenate((zero_padding, 0.2 * np.random.normal(size=len(t)), zero_padding))

# 4. Pulse Current Stimulation (PCS) - Periodic pulses
# Create a signal with periodic pulses
pcs_signal = np.zeros_like(t)  # Start with a zero signal
pulse_width = 50               # Define pulse width
pulse_interval = 80           # Define interval between pulses

# Generate pulse train
for i in range(0, len(t), pulse_interval):
    pcs_signal[i:i + pulse_width] = 0.5  # Set pulse height to 0.5
    print(i)

# Pad the pulse train signal with zeros
pcs_signal = np.concatenate((zero_padding, pcs_signal, zero_padding))

# Monophasic square, biphasic square, monophasic sinusoidal, biphasic sinusoidal

# Mono square
pcs_mono_square = ute.create_square_pulse(10.0, 1000, 1.0)
midpoint = len(pcs_mono_square) // 2
pcs_mono_square[midpoint:] = 0

print(np.shape(pcs_mono_square))

# Bi square
pcs_bi_square = ute.create_square_pulse(10.0, 1000, 1.0)

# Mono sawtooth
pcs_mono_sawtooth = ute.create_sawtooth_pulse(10.0, 1000, 1.0, first_peak='negative')
midpoint = len(pcs_mono_sawtooth) // 2
pcs_mono_sawtooth[midpoint:] = 0

# Bi sawtooth
pcs_bi_sawtooth = ute.create_sawtooth_pulse(10.0, 1000, 1.0, first_peak='negative')

# Mono sinusoidal
pcs_mono_sinu = ute.create_sin_pulse(10.0, 1000, 1.0)
midpoint = len(pcs_mono_sinu) // 2
pcs_mono_sinu[midpoint:] = 0

# Bi sinusoidal
pcs_bi_sinu  = ute.create_sin_pulse(10.0, 1000, 1.0)

pulses = [pcs_mono_square, pcs_bi_square, pcs_mono_sawtooth, pcs_bi_sawtooth, pcs_mono_sinu, pcs_bi_sinu]
pcs_signal = np.concatenate((
    zero_padding,
    pcs_mono_square,
    np.zeros(40),
    pcs_bi_square,
    np.zeros(80),
    pcs_mono_sawtooth,
    np.zeros(40),
    pcs_bi_sawtooth,
    np.zeros(80),
    pcs_mono_sinu,
    np.zeros(40),
    pcs_bi_sinu,
    zero_padding
))

# Updated time vector to match the length of the signals after padding
t_extended = np.linspace(0, 4 * np.pi + (100 / 1000) * 4 * np.pi, len(tdcs_signal))
t_extended_2 = np.linspace(0, 4 * np.pi + (100 / 1000) * 4 * np.pi, len(pcs_signal))

# Create the figure and axes for subplots
fig, axs = plt.subplots(2, 2, figsize=(10, 4), sharex=True)

# Plot tDCS signal
axs[0, 0].plot(t_extended, tdcs_signal, color='#5654FC', linewidth=2)
axs[0, 0].set_title('Transcranial Direct Current Stimulation (tDCS)', fontsize=12)
axs[0, 0].axis('off')  # Remove axis for a clean look

# Plot tACS signal
axs[0, 1].plot(t_extended, tacs_signal, color='#5654FC', linewidth=2)
axs[0, 1].set_title('Transcranial Alternating Current Stimulation (tACS)', fontsize=12)
axs[0, 1].axis('off')  # Remove axis for a clean look

# Plot tRNS signal
axs[1, 0].plot(t_extended, trns_signal, color='#5654FC', linewidth=2)
axs[1, 0].set_title('Transcranial Random Noise Stimulation (tRNS)', fontsize=12)
axs[1, 0].axis('off')  # Remove axis for a clean look

# Plot PCS signal
axs[1, 1].plot(t_extended_2, pcs_signal, color='#5654FC', linewidth=2)
axs[1, 1].set_title('Pulse Current Stimulation (PCS)', fontsize=12)
axs[1, 1].axis('off')  # Remove axis for a clean look

# Adjust layout to prevent overlapping and display the plot
plt.tight_layout()
plt.show()

# Save
# plt.savefig(f'new_signals.png', dpi=300, bbox_inches='tight', transparent=True)
