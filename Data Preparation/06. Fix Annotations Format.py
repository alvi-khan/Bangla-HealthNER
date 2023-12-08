import json
import pandas as pd
import os


def get_outputs(data):
    outputs = []

    for j, sample in enumerate(data['annotations']):
        text = sample[0]
        entities = {'start': [], 'end': [], 'label': []}

        for entity in sample[1]['entities']:
            start = entity[0]
            end = entity[1]
            label = entity[2]
            if len(entities['end']) > 0:
                assert start > entities['end'][
                    -1], f"Erroneous entity positions in file {annotations_path}{folder_name}/{file} sample {j + 1}"
            entities['start'].append(start)
            entities['end'].append(end)
            entities['label'].append(label)

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
        assert len(output) == len(
            text.split()), f"Lengths not matching in file {annotations_path}{folder_name}/{file} for sample {j + 1}: {output}, {text.split()}"
        remove = [i for i, word in enumerate(text.split()) if word in ['Question:', 'Answer:']]
        for i in range(1, len(remove)):
            outputs += [output[remove[i - 1] + 1: remove[i]]]
        outputs += [output[remove[-1] + 1:]]

    return outputs


labels = []
texts = []
df = pd.read_json(r"./data.json")

annotations_path = "./Unshuffled Annotations/"
for folder_name in os.listdir(annotations_path):
    if not os.path.isdir(f"{annotations_path}{folder_name}"):
        continue

    files = os.listdir(f"{annotations_path}{folder_name}")
    files.sort()
    for j, file in enumerate(files):
        file_name = file.replace("data-", "")
        file_name = file_name.replace(".json", "")

        i = int(file_name)

        count = 100
        with open(f"{annotations_path}{folder_name}/{file}", encoding="utf-8") as f:
            data = json.load(f)
            # First file has control group. Exclude.
            if j == 0:
                data['annotations'] = data['annotations'][25:]
                count = 75

        assert len(data['annotations']) == count, f"Not {count} Samples in file {annotations_path}{folder_name}/{file}."

        labels += get_outputs(data)
        out = df.iloc[i - 100: i]
        # First file has control group. Exclude.
        if j == 0:
            out = df.iloc[i - 100 + 25: i]
        for index, row in out.iterrows():
            texts.append(row['question'])
            for answer in row['answers']:
                texts.append(answer)

out = pd.DataFrame({'text': texts, 'labels': labels})
out = out[~out['text'].isin(out['text'][out['text'].duplicated()])]
out.to_json('data.json')
