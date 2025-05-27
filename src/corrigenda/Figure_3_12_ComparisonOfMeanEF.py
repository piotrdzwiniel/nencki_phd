import pandas as pd
import matplotlib.pyplot as plt

# Creating a DataFrame with the given data
data = {
    'Volume': ['Scalp', 'Eyeballs', 'Optic Nerve', 'Rest of the Brain'],
    'Mean': [0.0047, 0.0281, 0.0092, 0.0034],
    'Sum': [0, 0, 0, 0],
    'SD': [0.0255, 0.0061, 0.0035, 0.0018],
    'Count': [12200200, 17542, 1637, 1638915],
    'Max': [1.1292, 0.0444, 0.0352, 0.0186],
    'Min': [0.0, 0.0145, 0.0047, 0.0000]
}
df = pd.DataFrame(data)

# Plotting the data side by side
plt.figure(figsize=(6, 4))  # A4 size in inches (landscape orientation)

# Subplot for Mean values comparison with SD error bars

plt.bar(df['Volume'], df['Mean'], yerr=df['SD'], color='black', alpha=0.5, edgecolor='black', capsize=5)
plt.ylabel('Mean EFM (V/m)', fontsize=12)
plt.title('Comparison of Mean Electric Field (with SD)', fontsize=14, pad=20)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)

# Set ylim 0-0.7 and set tick with 0.1 step
plt.ylim(0, 0.08)
plt.yticks([0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08])

# Subplot for Sum values comparison
# plt.subplot(1, 2, 2)
# plt.bar(df['Volume'], df['Sum'], color='black', alpha=0.5, edgecolor='black')
# plt.ylabel('Sum of EFM (V/m)', fontsize=12)
# plt.title('Total Electric Field Across Volumes', fontsize=14, pad=20)
# plt.xticks(rotation=45, fontsize=12)
# plt.yticks(fontsize=12)

# Set ylim to 70000 and step to 10000
# plt.ylim(0, 80000)
# plt.yticks([0, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000])

plt.tight_layout()
plt.subplots_adjust(wspace=0.3)
# plt.show()
plt.savefig('Corrigenda Figure 3-12A.png', dpi=300, bbox_inches='tight', transparent=True)