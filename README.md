# NERvous About My Health: Constructing a Bengali Medical Named Entity Recognition Dataset

This repository contains the data and code of ['NERvous About My Health: Constructing a Bengali Medical Named Entity Recognition Dataset'](https://aclanthology.org/2023.findings-emnlp.383/), published in the **Findings of the Association for Computational Linguistics**, at **The 2023 Conference on Empirical Methods in Natural Language Processing (EMNLP)**.

All of the code and the dataset are being provided under the [CC BY-NC-SA 4.0 License](https://creativecommons.org/licenses/by-nc-sa/4.0/). The code provided can be used to re-create the data preparation process we followed, as well as the training and evaluation of the benchmark models.

The repository is divided into the following sections:

- [`Data Preparation`](Data%20Preparation): Contains the scripts used to collect, clean and prepare the final dataset. Extensive details are provided in [this README file](./Data%20Preparation/README.md).

- [`Dataset`](Dataset): Contains the final release of the Bangla-HealthNER dataset. The dataset is being provided in the form of separate training, validation and test sets to allow our experiments to be reproduced without the additional noise caused by mismatched data shuffling.

- [`train.ipynb`](train.ipynb): The training script used to train and evaluate the benchmark models.

- [`ChatGPT`](ChatGPT): Contains the scripts used to prompt and evaluate GPT 3.5, the results of which are reported in Table 3.

- [`Graphics`](Graphics): Contains the scripts used to create the graphs presented in the paper.


## Citation

```
@inproceedings{khan-etal-2023-nervous,
    title     = "{NER}vous About My Health: Constructing a {B}engali Medical Named Entity Recognition Dataset",
    author    = "Khan, Alvi and Kamal, Fida and Nower, Nuzhat and Ahmed, Tasnim and Ahmed, Sabbir and Chowdhury, Tareque",
    editor    = "Bouamor, Houda and Pino, Juan and Bali, Kalika",
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2023",
    month     = dec,
    year      = "2023",
    address   = "Singapore",
    publisher = "Association for Computational Linguistics",
    url       = "https://aclanthology.org/2023.findings-emnlp.383",
    doi       = "10.18653/v1/2023.findings-emnlp.383",
    pages     = "5768--5774",
    abstract  = "The ability to identify important entities in a text, known as Named Entity Recognition (NER), is useful in a large variety of downstream tasks in the biomedical domain. This is a considerably difficult task when working with Consumer Health Questions (CHQs), which consist of informal language used in day-to-day life by patients. These difficulties are amplified in the case of Bengali, which allows for a huge amount of flexibility in sentence structures and has significant variances in regional dialects. Unfortunately, the complexity of the language is not accurately reflected in the limited amount of available data, which makes it difficult to build a reliable decision-making system. To address the scarcity of data, this paper presents {`}Bangla-HealthNER{'}, a comprehensive dataset designed to identify named entities in health-related texts in the Bengali language. It consists of 31,783 samples sourced from a popular online public health platform, which allows it to capture the diverse range of linguistic styles and dialects used by native speakers from various regions in their day-to-day lives. The insight into this diversity in language will prove useful to any medical decision-making systems that are developed for use in real-world applications. To highlight the difficulty of the dataset, it has been benchmarked on state-of-the-art token classification models, where BanglishBERT achieved the highest performance with an F1-score of $56.13 \pm 0.75${\%}. The dataset and all relevant code used in this work have been made publicly available."
}
```