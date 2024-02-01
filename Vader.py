import pandas as pd

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('excel/tokenized_dataset.csv')

df['text_column'].fillna('', inplace=True)

analyzer = SentimentIntensityAnalyzer()

df['compound'] = df['tokenized_text'].apply(lambda x: analyzer.polarity_scores(x)['compound'])

def label_sentiment(compound):
    if compound >= 0.5:
        return 'positive'
    if compound <= -0.05:
        return 'negative'
    if compound >-0.05 and compound <0.05:
        return 'neutral'

df['sentiment'] = df['compound'].apply(label_sentiment)

# plt.figure(figsize=(10, 6))
# sns.countplot(x='sentiment', data=df, palette='viridis')
# plt.title('Sentiment Analysis Results')
# plt.xlabel('Sentiment')
# plt.ylabel('Count')
# plt.show()

import pickle

# Export the list to a file
with open('exported_data.pkl', 'wb') as file:
    pickle.dump(df, file)


sentiment_counts = df['sentiment'].value_counts()

# # Plotting the pie chart
# plt.figure(figsize=(4, 4))
# plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140, colors=['red', 'yellow', 'green'])
# plt.title('Sentiment Analysis Distribution')
# plt.show()


# Print the DataFrame
print(df[['text_column', 'compound', 'sentiment']])
