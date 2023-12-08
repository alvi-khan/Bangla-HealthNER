import pandas as pd
from sklearn.model_selection import train_test_split

DATA_PATH = "./data.json"

df = pd.read_json(DATA_PATH)

print(f"Total Samples: {len(df)}")

train, valid = train_test_split(df, test_size=0.2)
valid, test = train_test_split(valid, test_size=0.5)

print(f"Training Set: {len(train)}")
print(f"Validation Set: {len(valid)}")
print(f"Test Set: {len(test)}")

train.to_json('../Dataset/train.json', orient="records")
valid.to_json('../Dataset/valid.json', orient="records")
test.to_json('../Dataset/test.json', orient="records")
