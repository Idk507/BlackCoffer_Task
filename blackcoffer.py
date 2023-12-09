import pandas as pd
import os
import nltk
import spacy
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import nltk
from textstat import flesch_kincaid_grade, syllable_count


df = pd.read_excel('input.xlsx')

output_directory = 'extracted_articles'
os.makedirs(output_directory, exist_ok=True)
for index, row in df.iterrows():
    url = row['URL']
    url_id = row['URL_ID']

   
    response = requests.get(url)

    if response.status_code == 200:
       
        soup = BeautifulSoup(response.content, 'html.parser')

       
        title = soup.find('title').get_text()

       
        article_text = ''
        for paragraph in soup.find_all('p'):
            article_text += paragraph.get_text() + '\n'

        
        output_file_path = os.path.join(output_directory, f'{url_id}.txt')
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(f'Title: {title}\n\n')
            file.write(article_text)

        print(f'Saved article from {url_id} to {output_file_path}')
    else:
        print(f'Failed to fetch data from {url_id}')

print('Data extraction completed.')


input_directory = 'extracted_articles'
output_structure_file = 'Output Data Structure.xlsx'
output_file = 'analysis.xlsx'


nltk.download('punkt')
nlp = spacy.load('en_core_web_sm')


output_structure_df = pd.read_excel(output_structure_file)
output_df = pd.DataFrame(columns=output_structure_df.columns)

input_directory = 'extracted_articles'
output_structure_file = 'Output Data Structure.xlsx'
output_file = 'output.xlsx'

output_structure_df = pd.read_excel(output_structure_file)
output_df = pd.DataFrame(columns=output_structure_df.columns)
nltk.download('punkt')
nlp = spacy.load('en_core_web_sm')


for filename in os.listdir(input_directory):
    if filename.endswith('.txt'):
        file_path = os.path.join(input_directory, filename)

        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        
        analysis = TextBlob(text)

        
        tokens = nltk.word_tokenize(text)

        
        complex_word_count = 0
        for token in tokens:
            if flesch_kincaid_grade(token) > 10:  
                complex_word_count += 1
        percentage_complex_words = (complex_word_count / len(tokens)) * 100 if len(tokens) > 0 else 0

        
        fog_index = flesch_kincaid_grade(text)

        
        syllables = syllable_count(text)
        syllables_per_word = syllables / len(tokens) if len(tokens) > 0 else 0
        #print(syllables_per_word)
        num_words = len(tokens)
        num_sentences = len(nltk.sent_tokenize(text))
        doc = nlp(text)
        num_entities = len(doc.ents)
        
        word_length = sum(len(word) for word in tokens) / num_words if num_words > 0 else 0
        data = {
            'URL_ID': filename[:-4],
            'POSITIVE SCORE': analysis.sentiment.polarity,
            'NEGATIVE SCORE': analysis.sentiment.subjectivity,
            'POLARITY SCORE': analysis.sentiment.polarity,
            'SUBJECTIVITY SCORE': analysis.sentiment.subjectivity,
            'AVG SENTENCE LENGTH': len(nltk.sent_tokenize(text)),
            'PERCENTAGE OF COMPLEX WORDS': percentage_complex_words,
            'FOG INDEX': fog_index,
            'AVG NUMBER OF WORDS PER SENTENCE': len(tokens) / len(nltk.sent_tokenize(text)),
            'COMPLEX WORD COUNT': complex_word_count,
            'WORD COUNT': len(tokens),
            'SYLLABLE PER WORD': syllables_per_word,
            'PERSONAL PRONOUNS': text.lower().count('i') + text.lower().count('me') + text.lower().count('my'),
            'AVG WORD LENGTH': sum(len(word) for word in tokens) / len(tokens) if len(tokens) > 0 else 0,
            'Num_Words': num_words,
            'Num_Sentences': num_sentences,
            'Word_Length': word_length,
            'Num_Entities': num_entities,
        }

        #
        output_df = pd.concat([output_df, pd.DataFrame(data, index=[0])], ignore_index=True)


output_df.to_excel(output_file, index=False)

print(f'Text analysis completed. Results saved in {output_file}')



