import pandas as pd
import re
import os
import json
from tqdm import tqdm
import string


def fix_encoding(data):
    text = re.sub(r'\\u0985\\u09be', r'\\u0986', data)
    text = re.sub("অা", "আ", text)

    text = re.sub('“', '"', text)
    text = re.sub(r'\\u201c', r'\\u0022', text)

    text = re.sub('”', '"', text)
    text = re.sub(r'\\u201d', r'\\u0022', text)

    text = re.sub("‘", "'", text)
    text = re.sub(r'\\u2018', r'\\u0027', text)

    text = re.sub("’", "'", text)
    text = re.sub(r'\\u2019', r'\\u0027', text)

    text = re.sub("۔", ".", text)
    text = re.sub(r'\\u06d4', r'\\u002e', text)

    return text


def fix_punctuation_spacing(df):
    string = re.sub("([" + re.escape(punctuation) + "])", r" \1 ", df['question'])
    string = re.sub(u"\u09f7", u" \u09f7 ", string)
    string = re.sub(u"\u0964", u" \u0964 ", string)
    string = re.sub('\s{2,}', ' ', string)
    df['question'] = string

    answers = []

    for answer in df['answers']:
        string = re.sub("([" + re.escape(punctuation) + "])", r" \1 ", answer)
        string = re.sub(u"\u09f7", u" \u09f7 ", string)
        string = re.sub(u"\u0964", u" \u0964 ", string)
        string = re.sub('\s{2,}', ' ', string)
        answers.append(string)
    df['answers'] = answers
    return df


directory = '../data/'
punctuation = string.punctuation

for filename in tqdm(os.listdir(directory)):
    if not filename.endswith('.json'):
        continue

    f = os.path.join(directory, filename)
    if not os.path.isfile(f):
        continue

    data = None
    with open(f, encoding='utf-8') as file:
        data = file.read()

    if data is None:
        continue

    data = fix_encoding(data)

    df = json.loads(data)
    df = fix_punctuation_spacing(df)

    with open(f, 'w', encoding='utf-8') as file:
        file.write(json.dumps(df))
