import numpy as np
import matplotlib.pyplot as plt

# Function to generate FFT-based band-limited noise
def fftnoise(f):
    f = np.array(f, dtype='complex')
    Np = (len(f) - 1) // 2
    phases = np.random.rand(Np) * 2 * np.pi
    phases = np.cos(phases) + 1j * np.sin(phases)
    f[1:Np+1] *= phases
    f[-1:-1-Np:-1] = np.conj(f[1:Np+1])
    return np.fft.ifft(f).real

# Function to generate band-limited noise between min_freq and max_freq
def band_limited_noise(min_freq, max_freq, samples, samplerate):
    freqs = np.abs(np.fft.fftfreq(samples, 1/samplerate))
    f = np.zeros(samples)
    idx = np.where(np.logical_and(freqs >= min_freq, freqs <= max_freq))[0]
    f[idx] = 1
    return fftnoise(f)


# Function to generate band-limited Gaussian noise
def band_limited_gaussian_noise(min_freq, max_freq, samples, samplerate):
    freqs = np.abs(np.fft.fftfreq(samples, 1 / samplerate))
    f = np.zeros(samples, dtype='complex')  # FFT of the noise will be complex-valued
    idx = np.where(np.logical_and(freqs >= min_freq, freqs <= max_freq))[0]

    # Create a Gaussian-distributed random noise spectrum within the frequency range
    f[idx] = np.random.randn(len(idx)) + 1j * np.random.randn(
        len(idx))  # Gaussian-distributed complex noise
    return fftnoise(f)

# Parameters for the band-limited noise (for the third plot)
min_freq = 100  # Minimum frequency in Hz
max_freq = 640  # Maximum frequency in Hz
samplerate = 16000  # Sampling rate in Hz
duration = 0.5  # Duration of the noise signal in seconds (500 ms)
amplitude = 100  # Maximum amplitude in microamperes (µA)

# Calculate the number of samples for 500 ms
samples = int(samplerate * duration)

# Generate band-limited noise
noise_signal = band_limited_gaussian_noise(min_freq, max_freq, samples, samplerate)

# Normalize the signal to the desired amplitude (100 µA)
noise_signal = noise_signal / np.max(np.abs(noise_signal)) * amplitude

# General parameters for other signals
sampling_rate = 10000  # Sampling rate in Hz for precision

# 1. Single sinusoidal current pulse (100 ms, 10 Hz, 100 µA)
t1 = np.linspace(0, 0.1, int(sampling_rate * 0.1))  # Time vector for 100 ms
amplitude1 = 100  # Amplitude in microamperes
frequency1 = 10  # Frequency in Hz
signal1 = amplitude1 * np.sin(2 * np.pi * frequency1 * t1)

# 2. Sine wave (500 ms, 10 Hz, 100 µA)
t2 = np.linspace(0, 0.5, int(sampling_rate * 0.5))  # Time vector for 500 ms
amplitude2 = 100  # Amplitude in microamperes
frequency2 = 10  # Frequency in Hz
signal2 = amplitude2 * np.sin(2 * np.pi * frequency2 * t2)

# 3. Band-limited Gaussian random noise (500 ms, 100-640 Hz, max amplitude 100 µA)
t3 = np.linspace(0, 0.5, samples)  # Time vector for 500 ms

# Create figure and subplots with shared x-axis
fig, axs = plt.subplots(3, 1, figsize=(3, 4), sharex=True)

# Color Alpha Value
alpha_color = 0.6

# 1st Plot: Single sinusoidal current pulse
axs[0].plot(t1, signal1, color='black', linewidth=1, alpha=0.1)
axs[0].fill_between(t1, signal1, where=signal1 >= 0, color='red', interpolate=True, alpha=alpha_color)
axs[0].fill_between(t1, signal1, where=signal1 < 0, color='blue', interpolate=True, alpha=alpha_color)
axs[0].set_title("PCS")
# axs[0].set_ylabel("Current (µA)")
axs[0].set_ylim([-110, 110])

# 2nd Plot: Sine wave (500 ms, 10 Hz, 100 µA)
axs[1].plot(t2, signal2, color='black', linewidth=1, alpha=0.1)
axs[1].fill_between(t2, signal2, where=signal2 >= 0, color='red', interpolate=True, alpha=alpha_color)
axs[1].fill_between(t2, signal2, where=signal2 < 0, color='blue', interpolate=True, alpha=alpha_color)
axs[1].set_title("ACS")
axs[1].set_ylabel("Current (µA)")
axs[1].set_ylim([-110, 110])

# 3rd Plot: Band-limited Gaussian noise (500 ms, 100-640 Hz, max amplitude 100 µA)
axs[2].plot(t3, noise_signal, color='black', linewidth=1, alpha=0.1)
axs[2].fill_between(t3, noise_signal, where=noise_signal >= 0, color='red', interpolate=True, alpha=alpha_color)
axs[2].fill_between(t3, noise_signal, where=noise_signal < 0, color='blue', interpolate=True, alpha=alpha_color)
axs[2].set_title("RNS")
axs[2].set_xlabel("Time (s)")
# axs[2].set_ylabel("Current (µA)")
axs[2].set_ylim([-110, 110])

# Set shared x-axis labels at 0.0, 0.25, and 0.5
axs[2].set_xticks([0.0, 0.25, 0.5])
axs[2].set_xticklabels(['0.0', '0.25', '0.5'])

# Adjust layout
plt.tight_layout()

# Display the plots
# plt.savefig('figure 2-1 signals.png', dpi=300)
plt.show()
