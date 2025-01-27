import matplotlib.pyplot as plt
import numpy as np
from holoviews.plotting.bokeh.styles import font_size  # Importing Bokeh styles (unused in this code)
from matplotlib.colors import ListedColormap, BoundaryNorm

# Data matrix representing procedure indices (rows represent segments, columns represent trials)
procedure_indices_part_4 = [
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [1, 2, 3, 4, 5, 6, 7, 8, 0]
]

# Convert data to a NumPy array for easier manipulation
matrix = np.array(procedure_indices_part_4)

# Define a custom colormap with 9 discrete colors using the 'viridis_r' colormap reversed
cmap = ListedColormap(plt.cm.viridis_r(np.linspace(0.0, 1, 9)))
norm = BoundaryNorm(np.arange(-0.5, 9.5, 1), cmap.N)  # Setting boundaries from -0.5 to 9.5 for discrete colors

# Plotting the matrix
plt.figure(figsize=(6.5, 12))
img = plt.imshow(matrix, cmap=cmap, norm=norm, aspect='auto')  # Display the matrix with colormap and normalization
cbar = plt.colorbar(img, ticks=np.arange(9), boundaries=np.arange(-0.5, 9.5, 1))  # Add colorbar with ticks
cbar.set_label("Trial Type", fontsize=12)  # Label for the colorbar
cbar.set_ticks(np.arange(9))  # Setting tick positions
cbar.set_ticklabels(np.arange(9), fontsize=12)  # Setting tick labels for colorbar
cbar.minorticks_off()  # Turn off minor ticks for clarity

# Setting axis labels and ticks with increased font size for better readability
plt.xticks(ticks=np.arange(matrix.shape[1]), labels=np.arange(1, matrix.shape[1] + 1), fontsize=12)
plt.yticks(ticks=np.arange(matrix.shape[0]), labels=np.arange(1, matrix.shape[0] + 1), fontsize=12)
plt.xlabel("Trial", fontsize=12)
plt.ylabel("Segment", fontsize=12)

# Adding text labels to each cell in the matrix for clarity
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        plt.text(j, i, matrix[i, j], ha='center', va='center',
                 color="black" if matrix[i, j] == 0 else "white",
                 fontsize=12, weight='normal')  # Label cells with values, adjusting text color based on value

plt.tight_layout()  # Adjust layout to ensure all elements fit within the figure area
plt.show()  # Display the plot
# Optionally save the plot as an image file
# plt.savefig('procedure_indices_long.png', dpi=300, bbox_inches='tight', transparent=True)
