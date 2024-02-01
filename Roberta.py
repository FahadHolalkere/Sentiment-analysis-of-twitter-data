import nltk
import csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from nltk.sentiment import SentimentIntensityAnalyzer
from tqdm.notebook import tqdm
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax

# MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
# tokenizer = AutoTokenizer.from_pretrained(MODEL)
# model = AutoModelForSequenceClassification.from_pretrained(MODEL)



# file_path = r'master.csv'

# df = pd.read_csv(file_path, quoting=csv.QUOTE_MINIMAL, doublequote=True, escapechar='\\', encoding='unicode_escape')



# def get_sentiment_score(text):
#     if isinstance(text, str) and text.strip(): 
#         encoded_text = tokenizer(text, return_tensors='pt')
#         output = model(**encoded_text)
#         scores = output[0][0].detach().numpy()
#         scores = softmax(scores)
#         sentiment_score = {
#             'neg' : scores[0],
#             'neu' : scores[1],
#             'pos' : scores[2]
#         }
#         return sentiment_score
#     else:
        
#         return { 'neg': 0.0, 'neu': 0.0, 'pos': 0.0}

# df[['neg', 'neu', 'pos']] = df['Comments'].apply(lambda text: pd.Series(get_sentiment_score(text)))


# output_file_path = r'tweet2.csv'
# df.to_csv(output_file_path, index=False)
df = pd.read_csv('excel/tweet2.csv')

mean_sentiment = df[['neg', 'neu', 'pos']].mean()


import pickle

with open('exported_data.pkl', 'wb') as file:
    pickle.dump(df, file)

# # Define labels and colors for the pie chart
# labels = ['Negative', 'Neutral', 'Positive']
# colors = ['red', 'gray', 'green']

# # Create a pie chart
# plt.pie(mean_sentiment, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)

# # Set plot title
# plt.title('Overall Sentiment Distribution')

# # Show the plot
# plt.show()