import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

# Load the CSV file into a Pandas DataFrame
csv_file_path = r"excel/tweet2.csv"
df = pd.read_csv(csv_file_path)

# Check and handle data types
df['Comments'] = df['Comments'].astype(str)

# Handle NaN values
df = df.dropna(subset=['Comments'])

import pickle

# Export the list to a file
with open('exported_data.pkl', 'wb') as file:
    pickle.dump(df, file)

# # Combine filtering conditions
# max_pos_comments = df[df['pos'] > df[['neg', 'neu']].max(axis=1)]['Comments'].tolist()
# max_neg_comments = df[df['neg'] > df[['pos', 'neu']].max(axis=1)]['Comments'].tolist()
# max_neu_comments = df[df['neu'] > df[['pos', 'neg']].max(axis=1)]['Comments'].tolist()

# # Adjust WordCloud parameters
# wordcloud_params = {
#     'width': 800,
#     'height': 400,
#     'background_color': "black",
#     'max_words': 100
# }

# # Create a Tkinter window
# window = tk.Tk()
# window.title("Sentiment Word Clouds")

# # Function to display WordCloud in Tkinter window
# def display_wordcloud(wordcloud, title):
#     fig, ax = plt.subplots(figsize=(10, 5))
#     ax.imshow(wordcloud, interpolation="bilinear")
#     ax.set_title(title)
#     ax.axis("off")

#     canvas = FigureCanvasTkAgg(fig, master=window)
#     canvas_widget = canvas.get_tk_widget()
#     canvas_widget.pack(expand=True, fill='both')

# # Maximum positive sentiment
# max_pos_wordcloud = WordCloud(**wordcloud_params).generate(' '.join(max_pos_comments))
# display_wordcloud(max_pos_wordcloud, 'Positive Sentiment')

# # Maximum negative sentiment
# max_neg_wordcloud = WordCloud(**wordcloud_params).generate(' '.join(max_neg_comments))
# display_wordcloud(max_neg_wordcloud, 'Negative Sentiment')

# # Maximum neutral sentiment
# max_neu_wordcloud = WordCloud(**wordcloud_params).generate(' '.join(max_neu_comments))
# display_wordcloud(max_neu_wordcloud, 'Neutral Sentiment')

# # Run the Tkinter event loop
# window.mainloop()
