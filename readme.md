## Instructions for running the script:

**1. Install dependencies:**

* pandas
* os
* nltk
* spacy
* requests
* bs4
* textblob

**2. Download necessary models:**

* `nltk.download('punkt')`
* `spacy.load('en_core_web_sm')`

**3. Prepare input and output directories:**

* `input_directory`: Place your text files here.
* `output_directory`: This directory will be created to store the extracted text from the URLs.
* `output_structure_file`: Excel file containing the desired output data structure.
* `output_file`: Excel file where the analysis results will be saved.

**4. Run the script:**

Bash

```
python blackcoffer.py
```

**5. Output:**

The script will generate two Excel files:

* `extracted_articles/URL_ID.txt`: Contains the extracted text for each URL.
* `output.xlsx`: Contains the analysis results for each text file.

## Approach:

1. **Data extraction:**

   * Reads URL list from an Excel file.
   * Fetches HTML content using requests library.
   * Extracts title and article text using BeautifulSoup.
   * Saves the extracted text to separate files.
2. **Text analysis:**

   * For each extracted text file:

     * Calculates sentiment score using TextBlob.
     * Tokenizes the text using NLTK.
     * Calculates various readability metrics:

       * Percentage of complex words
       * Flesch-Kincaid grade level
       * Average sentence length
       * Average words per sentence
       * Syllables per word
       * Average word length
     * Identifies personal pronouns and entities using spaCy.
   * Saves the calculated metrics to an Excel file.
