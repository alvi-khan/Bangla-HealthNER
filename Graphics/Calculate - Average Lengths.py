import pandas as pd
import matplotlib

matplotlib.rc('font', family='Times New Roman', size='11')
matplotlib.rc('pdf', fonttype=42)
matplotlib.rcParams['savefig.transparent'] = True

df = pd.concat([pd.read_json(x, encoding='utf-8') for x in
                ['../Dataset/train.json', '../Dataset/valid.json', '../Dataset/test.json']])

entity_lengths = {}

for label in df['labels']:
    length = 0
    type = ''
    for token in label:
        if token == 'O':
            continue
        if token.startswith('B') and length != 0:
            if type in entity_lengths:
                entity_lengths[type] += [length]
            else:
                entity_lengths[type] = [length]
            length = 0
        type = token[2:]
        length = length + 1
    if length == 0:
        continue
    if type in entity_lengths:
        entity_lengths[type] += [length]
    else:
        entity_lengths[type] = [length]

for key in entity_lengths:
    entity_lengths[key] = sum(entity_lengths[key]) / len(entity_lengths[key])

print(entity_lengths)
