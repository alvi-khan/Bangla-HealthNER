import json
import pandas as pd
import os


def get_outputs(annotation_file):
    outputs = []

    with open(annotation_file, encoding="utf-8") as f:
        data = json.load(f)

    if len(data['annotations']) > 25:
        data['annotations'] = data['annotations'][:25]
    assert len(data['annotations']) == 25, f"Not 25 Samples in file {annotation_file}."

    for i, sample in enumerate(data['annotations']):
        text = sample[0]
        entities = {'start': [], 'end': [], 'label': []}

        for entity in sample[1]['entities']:
            entities['start'].append(entity[0])
            entities['end'].append(entity[1])
            entities['label'].append(entity[2])

        output = []
        cursor = 0
        for i in range(len(entities['start'])):
            start = entities['start'][i]
            end = entities['end'][i]
            label = entities['label'][i]
            non_entities = text[cursor: start].split()
            tokens = text[start: end].split()
            output = output + ['O'] * len(non_entities) + [f'B-{label}'] + [f'I-{label}'] * (len(tokens) - 1)
            cursor = end
        non_entities = text[cursor:].split()
        output += ['O'] * len(non_entities)
        assert len(output) == len(text.split()), f"Lengths not matching: {output}, {text}"

        outputs.append(output)

    return outputs


df = pd.read_json("../data.json")

for file in os.listdir():
    if not file.endswith(".json"):
        continue

    with open(file, encoding="utf-8") as f:
        data = json.load(f)
        control_file = "../Control Groups/" + data['set'] + ".json"

    annotations = get_outputs(file)
    labels = get_outputs(control_file)
    out = pd.DataFrame({'labels': labels, 'annotations': annotations})
    out.to_json(f'output/{file}')
