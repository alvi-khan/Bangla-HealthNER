import pandas as pd
import matplotlib

matplotlib.rc('font', family='Times New Roman', size='11')
matplotlib.rc('pdf', fonttype=42)
matplotlib.rcParams['savefig.transparent'] = True

df = pd.concat([pd.read_json(x, encoding='utf-8') for x in
                ['../Dataset/train.json', '../Dataset/valid.json', '../Dataset/test.json']])

entities_counts = {}

for label in df['labels']:
    label = list(filter(lambda token: token.startswith('B'), label))
    for entity in label:
        if entity[2:] in entities_counts:
            entities_counts[entity[2:]] = entities_counts[entity[2:]] + 1
        else:
            entities_counts[entity[2:]] = 1

print(entities_counts)
