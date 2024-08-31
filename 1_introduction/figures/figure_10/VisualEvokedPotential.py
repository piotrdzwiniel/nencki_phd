import numpy as np
import matplotlib.pyplot as plt

# Czas (w ms)
time = np.linspace(0, 200, 1000)

# Tworzenie wzrokowego potencjału wywołanego
# Parametry dla załamków: amplituda, czas (w ms), szerokość
n75 = -5 * np.exp(-0.5 * ((time - 75) / 10) ** 2)
p100 = 10 * np.exp(-0.5 * ((time - 100) / 10) ** 2)
n135 = -7 * np.exp(-0.5 * ((time - 135) / 10) ** 2)

# Sumowanie załamków do stworzenia całego VEP
vep = n75 + p100 + n135

# Rysowanie wykresu
plt.figure(figsize=(8, 4))
plt.plot(time, vep, label='VEP', color='blue')
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(75, color='lightgray', linestyle='--', label='N75')
plt.axvline(100, color='gray', linestyle='--', label='P100')
plt.axvline(135, color='darkgray', linestyle='--', label='N135')

# Oznaczenia osi i tytuł
plt.title('Visual Evoked Potential (VEP)')
plt.xlabel('Time (ms)')
plt.ylabel('Amplitude (µV)')
plt.legend()
plt.grid(False)

# Wyświetlenie wykresu
plt.show()
