import pandas as pd
import nltk
from nltk.corpus import stopwords

import csv
import string

input_file_path = 'excel/master.csv'

output_file_path = 'excel/result.csv'

def remove_punctuation(text):
    
    return ''.join(char for char in text if char not in string.punctuation)


with open(input_file_path, 'r', encoding='utf-8', errors='ignore') as csv_input, open(output_file_path, 'w', newline='', encoding='utf-8') as csv_output:
    reader = csv.reader(csv_input)
    writer = csv.writer(csv_output)

    for row in reader:
        
        cleaned_row = [remove_punctuation(element) for element in row]
        
        writer.writerow(cleaned_row)


from nltk.tokenize import word_tokenize

nltk.download('stopwords')


input_file_path = 'excel/result.csv'

df = pd.read_csv(input_file_path, header=None, names=['text_column'])


stop_words = set(stopwords.words('english'))

def tokenize_and_remove_stopwords(text):
    tokens = word_tokenize(str(text))
    tokens = [token.lower() for token in tokens if token.isalnum() and token.lower() not in stop_words]
    return tokens


df['tokenized_text'] = df['text_column'].apply(tokenize_and_remove_stopwords)


output_file_path = 'excel/tokenized_dataset.csv'
df.to_csv(output_file_path, index=False)


print(df[['text_column', 'tokenized_text']])
