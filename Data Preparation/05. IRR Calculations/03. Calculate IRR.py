import pandas as pd
import os
import numpy as np
from sklearn.metrics import cohen_kappa_score, f1_score
import warnings

warnings.filterwarnings("ignore")


data_path = './output/'

file_scores = []
file_f1s = []

for file in os.listdir(data_path):
    df = pd.read_json(f'{data_path}/{file}', orient="columns")
    
    scores = [cohen_kappa_score(row['annotations'], row['labels']) for index, row in df.iterrows()]
    f1s = [f1_score(row['labels'], row['annotations'], average='weighted') for index, row in df.iterrows()]
    
    scores = [s if not np.isnan(s) else 1.0 for s in scores]
    
    file_scores.extend(scores)
    file_f1s.extend(f1s)

print("Average Cohen Kappa Score: ", sum(file_scores) / len(file_scores))
print("Average F1 Score: ", sum(file_f1s) / len(file_f1s))
