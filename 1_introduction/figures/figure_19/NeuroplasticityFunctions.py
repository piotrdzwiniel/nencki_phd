import numpy as np
import matplotlib.pyplot as plt

# Define the function f(x) = 1/x
def f(x):
    return 1 / x

# Define the signed log transformation function
def signed_log(x):
    return np.sign(x) * np.log1p(np.abs(x))

# Generate 2000 x values from -100 to 100, excluding 0 to avoid division by zero
x = np.linspace(-100, 100, 2000)
x = x[x != 0]  # Remove 0 from the array to avoid division by zero

# Calculate the corresponding y values
y = f(x)

# Apply signed log transformation to x and y values
x_log = signed_log(x)
y_log = signed_log(y)

# Create the plot
plt.figure(figsize=(5, 4))  # Adjusting figure size to make it more square-like

# Plot the function with different colors for positive and negative x values
plt.plot(x_log[x > 0], y_log[x > 0], 'r', linewidth=1)  # Outline in red for positive x values
plt.plot(x_log[x < 0], y_log[x < 0], 'b', linewidth=1)  # Outline in blue for negative x values

# Fill the area under the curve for positive and negative parts
plt.fill_between(x_log, y_log, where=(x > 0), color='red', alpha=0.6)
plt.fill_between(x_log, y_log, where=(x < 0), color='#5654FC', alpha=0.6)

# Add black lines for the x and y axes
plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)

# Set axis labels and move them to desired positions
plt.xlabel(r'$\Delta t$', fontsize=14)
plt.ylabel(r'$\Delta s$', fontsize=14)

# Move the xlabel to the top
plt.gca().xaxis.set_label_coords(1, 0.47)
# Move the ylabel to the right
plt.gca().yaxis.set_label_coords(0.49, 1)

# Automatically set axis limits
plt.autoscale()

# Add text labels "LTP" and "LTD" closer to the curve center
plt.text(3, 1.2, 'potentiation', color='red', fontsize=16, fontweight='bold', ha='center')
plt.text(-3, -1.2, 'depression', color='#5654FC', fontsize=16, fontweight='bold', ha='center')

# Set aspect ratio to equal for a balanced plot
plt.gca().set_aspect('equal', adjustable='box')

# Remove grid
plt.grid(False)

# Remove figure spines (outlines)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)

# Remove ticks and tick labels
plt.xticks([])  # Remove x-axis ticks
plt.yticks([])  # Remove y-axis ticks

# Show the plot
plt.show()
