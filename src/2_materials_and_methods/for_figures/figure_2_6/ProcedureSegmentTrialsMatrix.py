import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap, BoundaryNorm

# Data: List of lists representing procedure's block 4 segments and trial types
procedure_indices_part_4 = [
    [2, 0, 6, 7, 5, 3, 4, 1, 9, 8],
    [9, 7, 4, 8, 1, 3, 0, 2, 5, 6],
    [0, 6, 9, 4, 2, 3, 5, 7, 1, 8],
    [9, 2, 1, 8, 0, 6, 7, 5, 3, 4],
    [2, 9, 8, 5, 6, 0, 3, 4, 7, 1],
    [3, 5, 7, 8, 0, 6, 9, 2, 4, 1],
    [1, 3, 0, 5, 4, 2, 8, 9, 7, 6],
    [1, 7, 2, 5, 3, 6, 9, 0, 8, 4],
    [1, 5, 8, 9, 2, 4, 6, 7, 0, 3],
    [5, 1, 6, 4, 2, 3, 7, 8, 0, 9],
    [7, 0, 2, 5, 4, 9, 3, 1, 6, 8],
    [6, 3, 8, 5, 4, 9, 1, 0, 7, 2],
    [0, 9, 7, 6, 2, 3, 5, 1, 4, 8],
    [0, 6, 7, 1, 4, 3, 5, 8, 2, 9],
    [5, 0, 3, 1, 2, 8, 9, 6, 7, 4]
]

# Convert data to a numpy array for easier manipulation
matrix = np.array(procedure_indices_part_4)

# Define a colormap with 10 discrete colors based on the 'viridis_r' colormap
cmap = ListedColormap(plt.cm.viridis_r(np.linspace(0.0, 1, 10)))
norm = BoundaryNorm(np.arange(-0.5, 10.5, 1), cmap.N)  # Define color boundaries for discrete colors

# Plotting the matrix
plt.figure(figsize=(6, 6))
img = plt.imshow(matrix, cmap=cmap, norm=norm, aspect='auto')  # Display the matrix as an image

# Adding a colorbar to indicate trial types
cbar = plt.colorbar(img, ticks=np.arange(10), boundaries=np.arange(-0.5, 10.5, 1))
cbar.set_label("Trial Type", fontsize=12)
cbar.set_ticks(np.arange(10))
cbar.set_ticklabels(np.arange(10), fontsize=12)
cbar.minorticks_off()

# Set tick labels and axis labels
plt.xticks(ticks=np.arange(matrix.shape[1]), labels=np.arange(1, matrix.shape[1] + 1), fontsize=12)
plt.yticks(ticks=np.arange(matrix.shape[0]), labels=np.arange(1, matrix.shape[0] + 1), fontsize=12)
plt.xlabel("Trial", fontsize=12)
plt.ylabel("Segment", fontsize=12)

# Adding text labels to each cell
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        # Display text inside each cell; color depends on the value (0 is displayed in black)
        plt.text(j, i, matrix[i, j], ha='center', va='center',
                 color="black" if matrix[i, j] == 0 else "white",
                 fontsize=12, weight='normal')

plt.tight_layout()  # Adjust layout to fit elements properly
plt.show()
# Optionally save the plot as an image
# plt.savefig('procedure_indices_part_4.png', dpi=300, bbox_inches='tight', transparent=True)
