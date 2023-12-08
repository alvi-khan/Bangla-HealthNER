import json
import os

directory = "../Unshuffled Annotations/"
for folder_name in os.listdir(directory):
    if not os.path.isdir(f"{directory}{folder_name}"):
        continue
    files = os.listdir(f"{directory}{folder_name}")
    files.sort()
    print(files)
    with open(f"{directory}{folder_name}/{files[0]}", encoding='utf-8') as f:
        data = json.load(f)
        control_group = data['annotations'][:25]

        with open(files[0][5:], 'w', encoding='utf-8') as file:
            json_data = {
                "set": folder_name[-6:-1],
                "classes": ["Symptom", "Health Condition", "Age", "Medicine", "Dosage", "Medical Procedure",
                            "Specialist"],
                "annotations": control_group
            }
            json.dump(json_data, file, ensure_ascii=False)
