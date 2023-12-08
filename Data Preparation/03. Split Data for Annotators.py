import pandas as pd
import math


def create_splits(files):
    for i in range(len(files) // 100):
        file_name = f'../split/{(i + 1) * 100}.txt'
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write('\n'.join(files[i * 100: (i + 1) * 100]))

    end = math.floor(len(files) // 100) * 100
    file_name = f'../split/{end + 100}.txt'
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write('\n'.join(files[end:]))


def create_string(data):
    string = ""
    string = string + "Question: " + data['question']
    for answer in data['answers']:
        string = string + " Answer: " + answer
    return string


df = pd.read_json('../data.json')

files = [create_string(row) for index, row in df.iterrows()]
create_splits(files)
