import random
import os
import pickle

directory = r"../split"
files = [x for x in os.listdir(directory) if x.endswith('.txt')]

data = []
for file in files:
    with open(os.path.join(directory, file), encoding='utf-8') as f:
        data.extend(f.readlines())

data = [x.replace("\n", "") for x in data]

indices = list(range(len(data)))

temp = list(zip(data, indices))
random.shuffle(temp)

shuffled_data, shuffled_indices = zip(*temp)
shuffled_data = list(shuffled_data)

for i in range(len(shuffled_data) // 100):
    file_name = f"./Shuffled Data/{files[i]}"
    with open(file_name, 'w', encoding='utf-8') as file:
        text = '\n'.join(shuffled_data[i * 100: (i + 1) * 100])
        file.write(text)

with open("indices", 'wb') as file:
    pickle.dump(shuffled_indices, file)
