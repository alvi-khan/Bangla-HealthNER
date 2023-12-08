import pandas as pd
from tqdm import tqdm
import json
import os

data_path = '../data'
df = pd.read_json('../data.json')

duplicates = {}
skip = []

print("Finding duplicate questions...")
for i in tqdm(range(len(df))):
    vals = df.index[df['question'] == df['question'][i]].tolist()   # get items with same question
    vals = [str(df['id'][x]) for x in vals]                         # get id column values of duplicates
    vals.remove(str(df['id'][i]))                                   # remove self id
    vals = [x for x in vals if x not in duplicates]                 # remove already registered
    if vals:
        duplicates[str(df['id'][i])] = vals

remaining = []

print("Deleting entries with duplicate questions...")
for key in tqdm(duplicates):
    if not os.path.isfile(f'{data_path}/{key}.json'):                    # duplicate of other key; already deleted
        continue
    
    main_file = f"{data_path}/{key}.json"
    main_df = pd.read_json(main_file)
    for dup_key in duplicates[key]:                                 # for each duplicate
        dup_file = f"{data_path}/{dup_key}.json"
        dup_df = pd.read_json(dup_file)
        
        # remove the main or the duplicate, whichever has empty answers
        if main_df.answers.empty and not dup_df.answers.empty:
            os.remove(main_file)
            main_file = dup_file
            main_df = dup_df
        elif not main_df.answers.empty and dup_df.answers.empty:
            os.remove(dup_file)
        elif main_df.answers.empty and dup_df.answers.empty:
            os.remove(dup_file)
        else:
            remaining.append((key, dup_key))                        # keep if both have answers (manual review)

print("The following duplicates require manual review:")
print(remaining)


print("Deleting duplicate answers in the same entries...")
for filename in tqdm(os.listdir(f"{data_path}/")):
    f = os.path.join(f"{data_path}/", filename)
    if not os.path.isfile(f):
        continue
    
    df = None
    
    with open(f) as file:
        df = json.loads(file.read())
    
    if df is None:
        continue
    
    answer_list = df['answers']
    answer_set = set(answer_list)
    if len(answer_set) != len(answer_list):
        df['answers'] = list(answer_set)
        with open(f'./{filename}', 'w') as file:
            file.write(json.dumps(df))
