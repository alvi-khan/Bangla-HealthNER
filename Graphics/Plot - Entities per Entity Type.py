import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

matplotlib.rc('font', family='Times New Roman', size='12')
matplotlib.rc('pdf', fonttype=42)
matplotlib.rcParams['savefig.transparent'] = True

data = {
    'Symptom': 33548,
    'Health\nCondition': 8171,
    'Medicine': 17862,
    'Specialist': 7024,
    'Age': 5585,
    'Dosage': 8006,
    'Medical\nProcedure': 3752,
}

fig = plt.figure(figsize=[6, 3.5])
colors = sns.color_palette("Blues_r", n_colors=8)

ax = sns.barplot(x=data.keys(), y=data.values(), palette=colors[1:8], width=0.70)
ax.set(xlabel=None)
ax.set(ylabel="No. of Distinct Entities")

for container in ax.containers:
    ax.bar_label(container, padding=3)

plt.margins(y=0.1)

fig.tight_layout()
plt.savefig('Entities per Entity Type.pdf', bbox_inches='tight', pad_inches=0)
plt.close(fig)
