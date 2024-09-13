import numpy as np
import matplotlib.pyplot as plt

# Generate data for dose and response
dose = np.linspace(0, 0.6, 100)  # Dose from 0 to 0.6 mV/mm
response = 1 / (1 + np.exp(-10 * (dose - 0.3)))  # Sigmoid function centered around 0.3

# Create a plot
plt.figure(figsize=(4, 5))

# Plot the dose-response curve
plt.plot(dose, response, color='black')

# Set the axis labels
plt.xlabel('Dose, mV/mm')
plt.ylabel('Minimum response, prob.')

# Set axis limits
plt.xlim(0, 0.6)
plt.ylim(0, 1)

# Set title
plt.title('Minimum effective dose')

# Add grid lines
plt.grid(True, linestyle='--', alpha=0.5)

# Display the plot
plt.tight_layout()
plt.show()
