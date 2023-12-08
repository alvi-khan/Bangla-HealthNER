import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from collections import Counter

matplotlib.rc('font', family='Times New Roman', size='11')
matplotlib.rc('pdf', fonttype=42)
matplotlib.rcParams['savefig.transparent'] = True

df = pd.concat([pd.read_json(x, encoding='utf-8') for x in ['train.json', 'valid.json', 'test.json']])

tokens = []
for label in df['labels']:
    label = [item[2:] for item in label if item != 'O']
    tokens.extend(label)

tokens = Counter(tokens)

fig = plt.figure(figsize=[3, 4])
colors = sns.color_palette("Blues_r", n_colors=len(tokens) + 1)

plt.pie(
    tokens.values(),
    labels=tokens.keys(),
    labeldistance=None,
    autopct='%1.1f%%',
    pctdistance=1.2,
    colors=colors[1:len(tokens) + 1]
)
plt.legend(loc='upper right')
centre_circle = plt.Circle((0, 0), 0.50, fc='white')
fig.gca().add_artist(centre_circle)
fig.tight_layout()
plt.savefig('Entity Distribution.pdf', bbox_inches='tight', pad_inches=0)
plt.close(fig)
