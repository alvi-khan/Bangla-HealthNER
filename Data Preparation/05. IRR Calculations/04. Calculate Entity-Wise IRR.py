import pandas as pd
import os
import numpy as np
from sklearn.metrics import f1_score
import warnings

warnings.filterwarnings("ignore")

data_path = './output/'

file_f1s = []
classes = ["O", "Symptom", "Health Condition", "Age", "Medicine", "Dosage", "Medical Procedure", "Specialist"]

for file in os.listdir(data_path):
    df = pd.read_json(f'{data_path}/{file}', orient="columns")

    f1s = [
        f1_score(
            [cls if cls == 'O' else cls[2:] for cls in row['labels']],
            [cls if cls == 'O' else cls[2:] for cls in row['annotations']],
            labels=classes,
            average=None,
            zero_division=np.nan
        ) for index, row in df.iterrows()
    ]
    f1s = pd.DataFrame(f1s, columns=classes)
    file_f1s.extend(f1s.values.tolist())

print("Average F1 Score: ")
print(pd.DataFrame(file_f1s, columns=classes).mean())
