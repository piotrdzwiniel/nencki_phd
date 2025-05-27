import pandas as pd
import matplotlib.pyplot as plt

# Creating a DataFrame with the given data
data = {
    'Volume': ['Scalp', 'Eyeballs', 'Optic Nerve', 'Rest of the Brain'],
    'Mean': [0.0012, 0.0370, 0.0144, 0.0037],
    'SD': [0.0049, 0.0100, 0.0102, 0.0009]
}
df = pd.DataFrame(data)

# Plotting the data side by side
plt.figure(figsize=(6, 4))  # A4 size in inches (landscape orientation)

# Subplot for Mean values comparison with SD error bars

plt.bar(df['Volume'], df['Mean'], yerr=df['SD'], color='black', alpha=0.5, edgecolor='black', capsize=5)
plt.ylabel('Mean CDM (A/m2)', fontsize=12)
plt.title('Comparison of Mean Current Density (with SD)', fontsize=14, pad=20)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)

# Set ylim 0-0.7 and set tick with 0.1 step
plt.ylim(0, 0.06)
plt.yticks([0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06])

plt.tight_layout()
plt.subplots_adjust(wspace=0.3)
# plt.show()
plt.savefig('Corrigenda Figure 3-19A.png', dpi=300, bbox_inches='tight', transparent=True)