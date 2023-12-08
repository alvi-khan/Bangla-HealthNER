import os
import pandas as pd
import glob
from tqdm import tqdm

pd.set_option('display.max_columns', None)

path_to_json = '../data/'

json_pattern = os.path.join(path_to_json, '*.json')
file_list = glob.glob(json_pattern)

dfs = []
for file in tqdm(file_list):
    data = pd.read_json(file, lines=True)
    data.insert(loc=0, column='id', value=os.path.basename(file.strip(".json")))
    dfs.append(data)

df = pd.concat(dfs, ignore_index=True)
df.to_json('../data.json', orient='records')
