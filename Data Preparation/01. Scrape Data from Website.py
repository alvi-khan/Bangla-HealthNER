import grequests
from bs4 import BeautifulSoup
import json
import time
import random
from os import path
from tqdm import tqdm

# parameters
base = "https://daktarbhai.com/services/ask-a-doctor/"
data_path = "./data/"
data_start = 148
data_end = 26469
batch_size = 5
min_sleep_time = 5
sleep_time_range = 10
time_penalty_size = 5


def retrieve_missing_records():
    skip = []
    ids = [i for i in range(data_start, data_end + 1) if not path.exists(f"{data_path}{i}.json")]
    ids = [i for i in ids if i not in skip]
    return ids


def process_record(record, filename):
    record = record.text
    soup = BeautifulSoup(record, "html.parser")
    data = soup.find('div', {"class": "popular-questions"})
    if data == None:
        return False

    question = data.find('a', {"class": "questions"}).find('h4', {"class": "questions-title"}).text.strip()

    answers = []
    for answer in data.find_all('div', {"class": "ans-info"}):
        answers.append(answer.find('p', recursive=False).text.strip())

    data = soup.find('div', {"class": "ques-meta details-meta"})
    date = data.find('p').text.strip()
    tag = data.find('a', {"class": "tag"})
    tag = tag.p.text.strip() if tag is not None else ""

    record = {
        'question': question,
        'answers': answers,
        'date': date,
        'tag': tag
    }

    with open(f"{filename}.json", "w") as outfile:
        json.dump(record, outfile)

    return True


def download_missing_records(ids):
    batch_start = 0 - batch_size
    batch_end = 0
    time_penalty = 0
    pbar = tqdm(total=len(ids), bar_format='{percentage:3.0f}%|{bar:20}| {n_fmt}/{total_fmt} {desc}')

    while len(ids) >= batch_end:
        batch_start = batch_start + batch_size
        batch_end = batch_end + batch_size

        sleep_start = min_sleep_time + time_penalty
        sleep_end = min_sleep_time + sleep_time_range + time_penalty
        time.sleep(random.uniform(sleep_start, sleep_end))

        batch = ids[batch_start:batch_end] if batch_end < len(ids) else ids[batch_start:]
        batch = [f"{base}{i}" for i in batch]
        rs = (grequests.get(url) for url in batch)
        batch_results = grequests.map(rs)

        errors = 0

        for i, result in enumerate(batch_results):
            pbar.update(1)
            try:
                success = process_record(record=result, filename=ids[batch_start + i])
                if not success:
                    errors = errors + 1
            except Exception as e:
                print(e)
                pass

        if errors == batch_size:
            time_penalty = time_penalty + time_penalty_size
            pbar.set_description(f"\033[91mTime Penalty increased to {time_penalty}\033[0m")
        elif time_penalty != 0:
            time_penalty = 0
            pbar.set_description("\033[92mTime Penalty reset\033[0m")

    pbar.close()


ids = retrieve_missing_records()
download_missing_records(ids)
