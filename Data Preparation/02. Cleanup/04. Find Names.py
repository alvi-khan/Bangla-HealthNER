from bnlp import NER
import os
import json
from tqdm import tqdm


bn_ner = NER()
model_path = "./name_detection/bn_ner.pkl"

common_nouns = ['ওয়ালিকুম', 'স্যার', 'ডিম', 'সিভিট', 'আস', 'আলাইকুম', 'এডোভাস', 'ওরস্যালাইন', 'প্যারাসিটামল', 'ওয়ালাইকুমুস', 'বাদাম', 'আমার', 'স্যুপ', 'নাপা', 'মিগ্রা', 'আসসালামু', 'ডাক্তার', 'খান', 'আব্বু', 'এলাট্রল', 'আম্মু', 'ভাত', 'অামার', 'চা', 'আদা', 'ইমোটিল', 'ডাঃ', 'ফলমূল', 'সুষম', 'ওষুধ', 'মেডিসিন', 'মধু', 'রস', 'একজন', 'সাহেব', 'এম', 'ট্যাবলেট', 'রেজিস্টার্ড', 'ভুষি', 'সবজি', 'লেবু', 'মিলিগ্রাম', 'ট্যাবলেট', 'ডায়েট']


def detect_name(text):
    if 'নাম' in text:
        return True
    
    result = bn_ner.tag(model_path, text)   # result format: [(word, tag), ...]
    
    name_present = any([x[0] not in common_nouns and x[1] == 'B-PER' and result[result.index(x) + 1][0] != 'খান' for x in result])

    if name_present:
        print(f"New: {text}")
        print()
        print(f"NER: {[x for x in result if '-PER' in x[1] and x[1] != 'S-PER']}")
        approval = input("Approve? (y/n): ")
        return True if approval == "y" else False
    
    return False


def process(df):
    os.system('cls')
    approved = detect_name(df['question'])
    if approved:
        return True
    
    for answer in df['answers']:
        approved = detect_name(answer)
        if approved:
            return True
    
    return False


with open('./name_detection/has_names.txt') as f:
    has_names = json.loads(f.read())

with open('./name_detection/false_positives.txt') as f:
    false_positives = json.loads(f.read())

for filename in tqdm(os.listdir('../data/')):
    f = os.path.join('../data/', filename)
    if not os.path.isfile(f):
        continue
    
    df = None
    with open(f, encoding='utf-8') as file:
        df = json.loads(file.read())
    
    if df is None:
        continue
    
    name_found = process(df)
    
    if name_found:
        has_names.append(df['id'])
        with open('./name_detection/has_names.txt', 'w') as f:
            f.write(json.dumps(has_names))
        continue
    
    false_positives.append(df['id'])
    with open('./name_detection/false_positives.txt', 'w') as f:
        f.write(json.dumps(false_positives))
