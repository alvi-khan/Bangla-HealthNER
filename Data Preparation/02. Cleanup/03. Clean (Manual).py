import re
import os
import json
from tqdm import tqdm
from gibberish_detector import gib_detect as gd


def remove_email(text):
    return re.sub("(([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\." \
                  "([a-z]{2,6}(?:\.[a-z]{2})?))(?![^<]*>)", "<EMAIL>", text)


def remove_numbers(text):
    return re.sub(r'\w*\d{5}\w*', '<NUMBER>', text).strip()


def remove_links(text):
    return re.sub(r'(https?://[^\s]+)', '<URL>', text)


def approve_changes(original_text, new_text):
    os.system('cls')
    print(f"Original: {original_text}")
    print()
    print(f"New: {new_text}")
    print()
    approval = input("Approve changes? (y/n): ")
    return True if approval == "y" else False


def confirm_spam(text):
    os.system('cls')
    print(text)
    approval = input("Is this spam? (y/n): ")
    return True if approval == "y" else False


def clean(df):
    modified = False
    is_spam = False

    text = df['question']
    if gd.is_gibberish(text):
        is_spam = confirm_spam(text)
        if is_spam:
            return is_spam, modified, df

    text = remove_email(text)
    text = remove_numbers(text)
    text = remove_links(text)

    if text != df['question']:
        approved = approve_changes(df['question'], text)
        if approved:
            df['question'] = text
            modified = True

    answers = []
    for answer in df['answers']:
        text = remove_email(answer)
        text = remove_numbers(text)
        text = remove_links(text)
        if text != answer:
            approved = approve_changes(answer, text)
            if approved:
                answer = text
                modified = True
        answers.append(answer)
    df['answers'] = answers

    return is_spam, modified, df


directory = '../data/'

for filename in tqdm(os.listdir(directory)):
    f = os.path.join(directory, filename)
    if not os.path.isfile(f):
        continue

    df = None
    with open(f, encoding='utf-8') as file:
        df = json.loads(file.read())

    if df is None:
        continue

    is_spam, modified, df = clean(df)

    if is_spam:
        os.remove(f)
        continue

    if modified:
        with open(f, 'w') as file:
            file.write(json.dumps(df))
