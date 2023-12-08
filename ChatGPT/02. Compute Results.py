import pandas as pd
import ast
from tqdm import tqdm
import evaluate

seqeval = evaluate.load("seqeval")
df = pd.read_json('./data.json', encoding='utf-8')

responses = []
labels = []

errors = []

for i in tqdm(range(len(df))):
    try:
        response = df['response'][i]
        response = response.replace('`', '"')
        response = ast.literal_eval(response)
        response = ['O' if entity[1] == 'Other' else entity[1] for entity in response]

        if len(df['labels'][i]) != len(response):
            continue

        if response[0] != 'O':
            response[0] = 'B-' + response[0]
        for j in range(1, len(response)):
            if response[j] == 'O':
                continue
            if response[j - 1] == 'O' or response[j - 1][2:] != response[j]:
                response[j] = 'B-' + response[j]
            else:
                response[j] = 'I-' + response[j]

        responses.append(response)
        labels.append(df['labels'][i])
    except:
        errors.append(i)
        continue

result = seqeval.compute(predictions=labels, references=responses, zero_division=0)
result = {
    "precision": result["overall_precision"],
    "recall": result["overall_recall"],
    "f1": result["overall_f1"],
    "accuracy": result["overall_accuracy"],
}

print(result)

print(errors)
