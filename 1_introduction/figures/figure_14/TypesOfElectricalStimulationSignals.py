import numpy as np
import matplotlib.pyplot as plt

# Time vector
t = np.linspace(0, 4 * np.pi, 1000)

# Periods of zeros before and after stimulation
zero_padding = np.zeros(50)

# 1. Transcranial Direct Current Stimulation (tDCS) - Constant DC offset
tdcs_signal = np.concatenate((zero_padding, np.ones_like(t) * 0.5, zero_padding))

# 2. Transcranial Alternating Current Stimulation (tACS) - Sinusoidal waveform
tacs_signal = np.concatenate((zero_padding, 0.5 * np.sin(5 * t), zero_padding))

# 3. Transcranial Random Noise Stimulation (tRNS) - Random noise
trns_signal = np.concatenate((zero_padding, 0.2 * np.random.normal(size=len(t)), zero_padding))

# 4. Pulse Current Stimulation (PCS) - Periodic pulses
pcs_signal = np.zeros_like(t)
pulse_width = 50
pulse_interval = 200

# Create pulse train
for i in range(0, len(t), pulse_interval):
    pcs_signal[i:i + pulse_width] = 0.5

pcs_signal = np.concatenate((zero_padding, pcs_signal, zero_padding))

# Updated time vector to match new signal lengths
t_extended = np.linspace(0, 4 * np.pi + (100 / 1000) * 4 * np.pi, len(tdcs_signal))

# Create the figure and axes
fig, axs = plt.subplots(2, 2, figsize=(10, 4), sharex=True)

# Plot tDCS signal
axs[0, 0].plot(t_extended, tdcs_signal, color='#5654FC', linewidth=2)
axs[0, 0].set_title('Transcranial Direct Current Stimulation (tDCS)', fontsize=12)
axs[0, 0].axis('off')

# Plot tACS signal
axs[0, 1].plot(t_extended, tacs_signal, color='#5654FC', linewidth=2)
axs[0, 1].set_title('Transcranial Alternating Current Stimulation (tACS)', fontsize=12)
axs[0, 1].axis('off')

# Plot tRNS signal
axs[1, 0].plot(t_extended, trns_signal, color='#5654FC', linewidth=2)
axs[1, 0].set_title('Transcranial Random Noise Stimulation (tRNS)', fontsize=12)
axs[1, 0].axis('off')

# Plot PCS signal
axs[1, 1].plot(t_extended, pcs_signal, color='#5654FC', linewidth=2)
axs[1, 1].set_title('Pulse Current Stimulation (PCS)', fontsize=12)
axs[1, 1].axis('off')

# Adjust layout and display the plot
plt.tight_layout()
plt.show()
