from scipy import signal
import matplotlib.pyplot as plt

# Definiowanie systemu
sys = ([1], [1, 2, 1])

# Obliczanie odpowiedzi impulsowej
time, y_amp = signal.impulse(sys)

# Normalizacja zakresu do nowych wymagań (0-1 dla X, 0-1.5 dla Y)
time_normalized = time / max(time)  # Skala od 0 do 1
y_amp_normalized = y_amp / max(y_amp) * 1.5  # Skala od 0 do 1.5

# Dodaj tutaj rozmiar figury
plt.figure(figsize=(5, 4))

# Rysowanie wykresu odpowiedzi impulsowej
plt.plot(time_normalized, y_amp_normalized, color='black', linewidth=2)

# Ustawienie etykiet osi
plt.title('Optimal noise level', fontsize=10)
plt.xlabel("Noise intensity")
plt.ylabel("Mutual information (bits)")

# Zakresy osi są teraz dopasowane do wymagań
plt.xlim(0, 1)
plt.ylim(0, 1.6)

# Wyświetlenie wykresu
plt.tight_layout()
plt.show()
