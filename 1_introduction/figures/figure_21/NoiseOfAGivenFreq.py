import numpy as np
import matplotlib.pyplot as plt

def fftnoise(f):
    f = np.array(f, dtype='complex')
    Np = (len(f) - 1) // 2
    phases = np.random.rand(Np) * 2 * np.pi
    phases = np.cos(phases) + 1j * np.sin(phases)
    f[1:Np+1] *= phases
    f[-1:-1-Np:-1] = np.conj(f[1:Np+1])
    return np.fft.ifft(f).real

def band_limited_noise(min_freq, max_freq, samples, samplerate):
    freqs = np.abs(np.fft.fftfreq(samples, 1/samplerate))
    f = np.zeros(samples)
    idx = np.where(np.logical_and(freqs>=min_freq, freqs<=max_freq))[0]
    f[idx] = 1
    return fftnoise(f)


a = 101
b = 640
samplerate = 16000
x = band_limited_noise(a, b, samples=500, samplerate=samplerate)
# x = np.int16(x * (2**15 - 1)) * 100
print(x, np.shape(x))

# NORMALIZE TO RANGE 0-1
# x = (x - np.min(x)) / (np.max(x) - np.min(x))  # Normalize in range 0-1
# lower, upper = -50, 50
# x = [lower + (upper - lower) * y for y in x.tolist()]
# NORMALIZE TO RANGE 0-1

# SET AMPLITUDE OF THE SIGNAL RNS
# First amplitude will be 50 uA and the second will be 100 uA
# Duration of the RNS signal will be 200, 300, 400 and 500 ms.

min_freq_in_hz, max_freq_in_hz = 101.0, 640.0  # High-frequency RNS based on Antal & Herrmann (2016)
pack_duration_in_s = [0.2, 0.3, 0.4, 0.5]  # Four durations based on other pack groups: 200, 300, 400 and 500 ms
pack_amplitude_in_ua = [50.0, 100.0]  # Two amplitudes based on other pack groups: 50 and 100 uA

# SET AMPLITUDE OF THE SIGNAL RNS

# TEST DISTRIBUTION
import seaborn as sb
sb.distplot(x)
# TEST DISTRIBUTION

plt.figure(figsize=(12, 4))
plt.plot(x, color='black', linewidth=1)
# plt.xlim(0, 10000)
# plt.axis('off')
# plt.savefig("%d_%d.png" % (a, b), transparent=True)
plt.show()
