import os
import pickle
import json

for folder_name in os.listdir("./Shuffled Annotations/"):
    if not os.path.isdir(f"./Shuffled Annotations/{folder_name}"):
        continue
    files = [x for x in os.listdir(f"./Shuffled Annotations/{folder_name}") if x.endswith('.json')]

    annotations = []
    for file in files:
        with open(f"./Shuffled Annotations/{folder_name}/{file}", encoding='utf-8') as f:
            data = json.load(f)
            annotations.extend(data['annotations'])

    indices = []

    with open(f"./Shuffled Data/{folder_name}/indices", 'rb') as f:
        indices = pickle.load(f)

    unshuffled_annotations = [val for (_, val) in sorted(zip(indices, annotations), key=lambda x: x[0])]

    if not os.path.exists(f"../Unshuffled Annotations/{folder_name}"):
        os.mkdir(f"../Unshuffled Annotations/{folder_name}")

    for i in range(len(unshuffled_annotations) // 100):
        file_name = f"../Unshuffled Annotations/{folder_name}/{files[i]}"
        with open(file_name, 'w', encoding='utf-8') as file:
            json_data = {
                "classes": ["Symptom", "Health Condition", "Age", "Medicine", "Dosage", "Medical Procedure",
                            "Specialist"],
                "annotations": unshuffled_annotations[i * 100: (i + 1) * 100]
            }
            json.dump(json_data, file, ensure_ascii=False)
