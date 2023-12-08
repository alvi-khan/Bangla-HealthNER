# Data Preparation

The dataset was prepared in a series of steps using several scripts, as outlined below:

## Step 01: Scraping the data from the website

[`01. Scrape Data from Website.py`](01.%20Scrape%20Data%20from%20Website.py)

Each question and the corresponding answers were stored in a separate file in a `data` folder. The filenames correspond to the IDs of the questions on the website. If you are following these instructions, please make sure to keep a backup of the downloaded files since the next steps modify the files.

## Step 2: Cleanup

[`01. Combine.py`](02.%20Cleanup/01.%20Combine.py)

Combines all the files into a single JSON, `data.json`. This file is the one we work with in the following steps.

[`02. Remove Duplicates.py`](02.%20Cleanup/02.%20Remove%20Duplicates.py)

Removes duplicate questions, retaining only one copy.
- The step deletes the files for the duplicate questions.
- A duplicate refers to exact matches. Very similar questions that were most likely spammed by the same author are not removed.
- Which duplicate to retain is determined based on which one has answers to the question.
- In cases where one or more duplicates all have answers, they are not deleted. These must be reviewed manually.
- Duplicate answers under the same question are removed.

[`03. Clean (Manual).py`](02.%20Cleanup/03.%20Clean%20(Manual).py)

Cleans the data. This process involves manual inspections.
- Spam questions are identified using a [gibberish detector](https://github.com/rrenaud/Gibberish-Detector). These are displayed on the terminal and must be manually approved before they are deleted. A copy of the source code for the gibberish detector is included.
- Emails, numbers (5 digits or more) and links in the question and each of the answers are removed using regex. Any changes must be approved before they are saved.

[`04. Find Names.py`](02.%20Cleanup/04.%20Find%20Names.py)

Named were identified using a [general Bangla NER model](https://pypi.org/project/bnlp-toolkit). A copy of the model is included.
- Each detection requires manual approval.
- The model frequently made erroneous detections on specific nouns. A list of such nouns was created over time and included in the script so such detections could be skipped.
- The IDs of the samples with names detected in them were stored. These names were then manually removed.

[`05. Clean (Auto).py`](02.%20Cleanup/05.%20Clean%20(Auto).py)

Fixes encoding, punctuation and spacing issues.

[`01. Combine.py`](02.%20Cleanup/01.%20Combine.py)

The cleaned files are combined back into a single JSON file, `data.json`.

## Step 3: Split Data

[`03. Split Data for Annotators.py`](03.%20Split%20Data%20for%20Annotators.py)

The data was split into groups of 100 samples. For ease of annotation, the questions and answers were joined to form a single string for each sample. They were marked with the prefixes 'QUESTION' and 'ANSWER' respectively so they could be separated again after annotation.

## Step 4: Annotation

1. The first 25 samples from each set of 100 samples were manually replaced with a control group.
2. Each set was then shuffled and provided to the annotators (refer to [`01.Shuffle.py`](04.%20Annotation/01.Shuffle.py)).
3. The annotators annotated each file using the [annotation tool](https://github.com/tecoholic/ner-annotator). They returned the annotations as JSON files. Each file has the following format:
```json
{
  "classes": ["Symptom", "Health Condition", "Age", "Medicine", "Dosage", "Medical Procedure", "Specialist"],
  "annotations": [
    [
      "Question: হালকা জ্বর র গলা ব্যাথা জন্য কি করতে হবে ?  Answer: আপনাকে ধন্যবাদ প্রশ্ন করার জন্য । আপনি ট্যাবলেট নাপা ৫০০ মিলিগ্রাম একটা করে খেতে পারেন । আদা , মধু , লেবু , গরম পানি খান । ধন্যবাদ । \r", 
      {
        "entities": [
          [10, 22, "Symptom"],
          [110, 128, "Medicine"],
          [129, 133, "Dosage"]
        ]
      }
    ],
    ...
  ]
}
```
4. The annotation files were checked to ensure they each had 100 annotations (refer to [`02. Check 100.py`](04.%20Annotation/02.%20Check%20100.py)).
5. Each of the annotation files was unshuffled (refer to [`03. Unshuffle Annotations.py`](04.%20Annotation/03.%20Unshuffle%20Annotations.py)).

## Step 5: IRR Calculations

[`01. Extract Control Group.py`](05.%20IRR%20Calculations/01.%20Extract%20Control%20Group.py)
Extracts the control groups from each file. The resulting files have the same format as the original files. We manually add one extra field to the JSON, `set`, which is used to identify which control group the file corresponds to.

[`02. Fix Format.py`](05.%20IRR%20Calculations/02.%20Fix%20Format.py)

Since the questions and answers were joined into a single string, they need to be separated again. The annotations also have to be adjusted accordingly. We process the annotated and original control groups to create a single file.

[`03. Calculate IRR.py`](05.%20IRR%20Calculations/03.%20Calculate%20IRR.py)

The output from the previous step is used to calculate the Cohen Kappa score and the weighted F1-Score row by row for each file and then averaged to find the IRR.

[`04. Calculate Entity-Wise IRR.py`](05.%20IRR%20Calculations/04.%20Calculate%20Entity-Wise%20IRR.py)

Calculates the entity-wise F1-Scores file by file and then averages them.

## Step 6: Fix formatting

[`06. Fix Annotations Format.py`](06.%20Fix%20Annotations%20Format.py)

This is the process as used in Step 5 to fix the data format, except it is being done for all the annotated data.

## Step 7: Split the data into train, valid and test files

[`07. Train, Valid, Test Split.py`](07.%20Train,%20Valid,%20Test%20Split.py)

Splits the data into train, validation and test sets.