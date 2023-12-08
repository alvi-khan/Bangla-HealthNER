import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

matplotlib.rc('font', family='Times New Roman', size='12')
matplotlib.rc('pdf', fonttype=42)
matplotlib.rcParams['savefig.transparent'] = True

data = {
    'Symptom': 3.96,
    'Health\nCondition': 2.33,
    'Medicine': 2.43,
    'Specialist': 2.09,
    'Age': 1.90,
    'Dosage': 4.91,
    'Medical\nProcedure': 2.37,
}

fig = plt.figure(figsize=[6, 3.5])
colors = sns.color_palette("Blues_r", n_colors=8)

ax = sns.barplot(x=data.keys(), y=data.values(), palette=colors[1:8], width=0.70)
ax.set(xlabel=None)
ax.set(ylabel="Average No. of Tokens per Entity")

for container in ax.containers:
    ax.bar_label(container, padding=3)

plt.margins(y=0.1)

fig.tight_layout()
plt.savefig('Average Lengths.pdf', bbox_inches='tight', pad_inches=0)
plt.close(fig)
