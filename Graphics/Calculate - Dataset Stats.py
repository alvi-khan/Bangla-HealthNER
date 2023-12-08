import pandas as pd
from collections import Counter

df = pd.read_json(r"./data.json")
print(f"Number of Samples: {len(df)}")

sentence_count = sum([len(text.replace('।', '.').split('.')) for text in df['text'].to_list()])
print(f"Number of Sentences: {sentence_count}")

average_length = sum([len(text) for text in df['text'].to_list()]) / len(df)
print(f"Average Sample Length: {average_length}")

tokens = []
for label in df['labels']:
    label = [item if item == 'O' else item[2:] for item in label]
    tokens.extend(label)
percentage_entity_tokens = ((len(tokens) - tokens.count('O')) / len(tokens)) * 100
print(f"Percentage of Entity Tokens: {percentage_entity_tokens}%")

print("Entity Distribution:")
print(Counter(tokens).items())
