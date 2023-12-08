import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

matplotlib.rc('font', family='Times New Roman', size='12')
matplotlib.rc('pdf', fonttype=42)
matplotlib.rcParams['savefig.transparent'] = True

data = {
    'Non\nEntity': 0.935450,
    'Symptom': 0.748917,
    'Health\nCondition': 0.809993,
    'Age': 0.895019,
    'Medicine': 0.948888,
    'Dosage': 0.836722,
    'Medical\nProcedure': 0.937678,
    'Specialist': 0.926978,
}

fig = plt.figure(figsize=[6.5, 3.5])
colors = sns.color_palette("Blues_r", n_colors=8)

ax = sns.barplot(x=data.keys(), y=data.values(), palette=colors, width=0.70)
ax.set(xlabel=None)
ax.set(ylabel="F1-Score (%)")
ax.set_ylim(0.7, 0.99)

for container in ax.containers:
    ax.bar_label(container, padding=3)

plt.margins(y=0.1)

fig.tight_layout()
plt.savefig('IAA per Entity Type.pdf', bbox_inches='tight', pad_inches=0)
plt.close(fig)
