import json
import os

directory = r"./Shuffled Annotations"
folders = os.listdir(directory)

for folder in folders:
    folder_path = os.path.join(directory, folder)
    
    if not os.path.isdir(folder_path):
        continue
    
    files = os.listdir(folder_path)
    for file in files:
        file_path = os.path.join(folder_path, file)
        
        with open(file_path, "rb") as f:
            data = json.load(f)
            annotations = len(data['annotations'])
            assert annotations == 100, f"{folder}/{file} has only {annotations} annotations"

print("All good!")
