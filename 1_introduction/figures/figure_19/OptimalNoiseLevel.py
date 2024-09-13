from scipy import signal
import matplotlib.pyplot as plt

# Define the transfer function of the system
# The system is defined by its numerator and denominator coefficients
# sys = (numerator, denominator)
sys = ([1], [1, 2, 1])

# Compute the impulse response of the system
# signal.impulse(sys) computes the impulse response of the linear time-invariant system
time, y_amp = signal.impulse(sys)

# Normalize the time range to [0, 1]
time_normalized = time / max(time)  # Scaling time to fit within the range [0, 1]

# Normalize the amplitude range to [0, 1.5]
y_amp_normalized = y_amp / max(y_amp) * 1.5  # Scaling amplitude to fit within the range [0, 1.5]

# Create the figure for plotting with a specific size
plt.figure(figsize=(5, 4))

# Plot the normalized impulse response
plt.plot(time_normalized, y_amp_normalized, color='black', linewidth=2)

# Set axis labels and title
plt.title('Optimal noise level', fontsize=10)
plt.xlabel("Noise intensity")  # X-axis label
plt.ylabel("Mutual information (bits)")  # Y-axis label

# Set the limits for the x and y axes according to the specified range
plt.xlim(0, 1)
plt.ylim(0, 1.6)

# Adjust layout for better spacing and presentation
plt.tight_layout()

# Display the plot
plt.show()
