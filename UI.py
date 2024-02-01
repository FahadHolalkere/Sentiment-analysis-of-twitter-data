import tkinter as tk
from tkinter import ttk
from wordcloud import WordCloud
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pickle
import subprocess

def compare_results():
    label.config(text="Comparison")

    # Assuming 'Vader.py' and 'Roberta.py' are scripts generating DataFrame and saving it to 'exported_data.pkl'
    subprocess.run(["python", "Vader.py"])
    with open('exported_data.pkl', 'rb') as file:
        df = pickle.load(file)

    # subprocess.run(["python", "Roberta.py"])
    # with open('exported_data.pkl', 'rb') as file:
    #     df1 = pickle.load(file)
    df1=pd.read_csv('excel/tweet2.csv')
    # Clear existing graphs
    clear_canvas()

    # Plotting the pie charts for sentiment distribution
    fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(10, 4))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(expand=True, fill='both')

    sentiment_counts = df['sentiment'].value_counts()
    mean_sentiment = df1[['neg', 'neu', 'pos']].mean()

    # Plotting the pie charts
    axs[0].pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140, colors=['red', 'yellow', 'green'])
    axs[0].set_title('Vader')

    axs[1].pie(mean_sentiment, labels=['Negative', 'Neutral', 'Positive'], autopct='%1.1f%%', startangle=140, colors=['red', 'yellow', 'green'])
    axs[1].set_title('Roberta')

    plt.style.use('ggplot')
    # Load the CSV files into Pandas DataFrames
    file1 = r"excel/tweets_with_robertasentiment.csv"
    file2 = r"excel/tweets_with_vadersentiment.csv"

    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Select only numeric columns (assuming "neg," "neu," and "pos" are numeric)
    numeric_columns1 = df1[['neg', 'neu', 'pos']]
    numeric_columns2 = df2[['neg', 'neu', 'pos']]

    mean_values1 = numeric_columns1.mean()
    mean_values2 = numeric_columns2.mean()
    combined_df = pd.concat([numeric_columns1, numeric_columns2], ignore_index=True)

    # Calculate the mean values for all sentiment categories across both files
    mean_values = combined_df.mean()

    # Set the figure size
    plt.figure(figsize=(10, 6))

    # Create a bar graph with adjusted x-coordinates for the second set of bars
    categories = np.arange(len(mean_values1))
    bar_width = 0.20
    space=0.03
    # Count of comments with scores for both CSV files
    count_comments1 = len(df1)
    count_comments2 = len(df2)
    total_comments = len(combined_df)


    print(f"Total number of comments: {count_comments1}")

    # Find the rows where 'neu' scores are the maximum
    max_neu_rows1 = df1[df1['neu'] == df1[['neg', 'neu', 'pos']].max(axis=1)]['neu']
    max_neu_rows2 = df2[df2['neu'] == df2[['neg', 'neu', 'pos']].max(axis=1)]['neu']
    max_neg_rows1 = df1[df1['neg'] == df1[['neg', 'neu', 'pos']].max(axis=1)]['neg']
    max_neg_rows2 = df2[df2['neg'] == df2[['neg', 'neu', 'pos']].max(axis=1)]['neg']
    max_pos_rows1 = df1[df1['pos'] == df1[['neg', 'neu', 'pos']].max(axis=1)]['pos']
    max_pos_rows2 = df2[df2['pos'] == df2[['neg', 'neu', 'pos']].max(axis=1)]['pos']



    print(f"Number of rows where 'neu' scores for roberta are the maximum: {len(max_neu_rows1)}")
    print(f"Number of rows where 'pos' scores for roberta are the maximum: {len(max_pos_rows1)}")
    print(f"Number of rows where 'neg' scores for roberta are the maximum: {len(max_neg_rows1)}")
    print(f"Number of rows where 'neu' scores for vader are the maximum: {len(max_neu_rows2)}")
    print(f"Number of rows where 'pos' scores for vader are the maximum: {len(max_pos_rows2)}")
    print(f"Number of rows where 'neg' scores for vader are the maximum: {len(max_neg_rows2)}")

    axs[2].bar(categories, mean_values1, width=bar_width,label='Roberta')
    axs[2].bar(categories + bar_width+space, mean_values2, width=bar_width, label='Vader')
    axs[2].bar(categories + 2 * (bar_width+space), mean_values, width=bar_width, label='Combined')

    # Add labels and title
    axs[2].xlabel('Sentiment Category')
    axs[2].ylabel('Mean Value')
    axs[2].title('Overall Sentiment Distribution')
    tick_labels = list(mean_values1.index)
    tick_labels[0] = 'Negative'
    tick_labels[1] = 'Neutral'
    tick_labels[2] = 'Positive'
    axs[2].xticks(categories + 1.5 * (bar_width + space), tick_labels)
    desired_ticks = 10
    axs[2].ylim(0, 0.55)
    axs[2].yticks(np.linspace(0, 0.55, 12))
    axs[2].legend()

    plt.tight_layout()
    plt.title('Sentiment Analysis Distribution')
    canvas.draw()

def generate_vader_results():
    label.config(text="Vader Results")

    # Assuming 'Vader.py' and 'Roberta.py' are scripts generating DataFrame and saving it to 'exported_data.pkl'
    subprocess.run(["python", "Vader.py"])
    with open('exported_data.pkl', 'rb') as file:
        df = pickle.load(file)

    # Clear existing graphs
    clear_canvas()

    sentiment_counts = df['sentiment'].value_counts()

    fig, axs = plt.subplots(1, 2, figsize=(15, 6))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(expand=True, fill='both')

    # Plotting the pie chart
    axs[0].pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140, colors=['red', 'yellow', 'green'])
    axs[0].set_title('Sentiment Distribution')

    # Plotting the bar chart
    sns.countplot(x='sentiment', data=df, palette='viridis', ax=axs[1])
    axs[1].set_title('Sentiment Analysis Results')
    axs[1].set_xlabel('Sentiment')
    axs[1].set_ylabel('Count')

    plt.tight_layout()
    canvas.draw()

def generate_roberto_results():
    label.config(text="Roberto Results")

    # subprocess.run(["python", "Roberta.py"])
    # with open('exported_data.pkl', 'rb') as file:
    #     df1 = pickle.load(file)
    df1=pd.read_csv('excel/tweet2.csv')
    # Clear existing graphs
    clear_canvas()

    mean_sentiment = df1[['neg', 'neu', 'pos']].mean()

    fig, axs = plt.subplots(1, 2, figsize=(15, 6))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(expand=True, fill='both')
    
    axs[0].pie(mean_sentiment, labels=['Negative', 'Neutral', 'Positive'], autopct='%1.1f%%', startangle=140, colors=['red', 'yellow', 'green'])
    axs[0].set_title('Roberta')

    categories = np.arange(len(mean_sentiment))
    bar_width = 0.25

    axs[1].bar(categories, mean_sentiment, width=bar_width, label='Roberta')

    # Add labels and title
    axs[1].set_xlabel('Sentiment Category')
    axs[1].set_ylabel('Mean Value')
    axs[1].set_title('Overall Sentiment Distribution')
    tick_labels = list(mean_sentiment.index)
    tick_labels[0] = 'Negative'
    tick_labels[1] = 'Neutral'
    tick_labels[2] = 'Positive'
    axs[1].set_xticks(categories)
    axs[1].set_xticklabels(tick_labels)
    axs[1].set_ylim(0, 0.55)
    axs[1].set_yticks(np.linspace(0, 0.55, 12))
    axs[1].legend()

    plt.tight_layout()
    plt.title('Sentiment Analysis Distribution')
    canvas.draw()

def generate_wordcount():
    # Assuming 'wordcount.py' is a script generating DataFrame and saving it to 'exported_data.pkl'
    subprocess.run(["python", "wordcount.py"])
    with open('exported_data.pkl', 'rb') as file:
        df2 = pickle.load(file)

    # Clear existing graphs
    clear_canvas()

    # Combine filtering conditions
    max_pos_comments = df2[df2['pos'] > df2[['neg', 'neu']].max(axis=1)]['Comments'].tolist()
    max_neg_comments = df2[df2['neg'] > df2[['pos', 'neu']].max(axis=1)]['Comments'].tolist()
    max_neu_comments = df2[df2['neu'] > df2[['pos', 'neg']].max(axis=1)]['Comments'].tolist()

    # Adjust WordCloud parameters
    wordcloud_params = {
        'width': 800,
        'height': 400,
        'background_color': "black",
        'max_words': 100
    }

    # Create a single figure with 3 subplots in one row
    fig = plt.figure(figsize=(18, 6))

    def display_wordcloud(wordcloud, title, position):
        ax = fig.add_subplot(1, 3, position)
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.set_title(title)
        ax.axis("off")

    # Maximum positive sentiment
    max_pos_wordcloud = WordCloud(**wordcloud_params).generate(' '.join(max_pos_comments))
    display_wordcloud(max_pos_wordcloud, 'Positive Sentiment', 1)

    # Maximum negative sentiment
    max_neg_wordcloud = WordCloud(**wordcloud_params).generate(' '.join(max_neg_comments))
    display_wordcloud(max_neg_wordcloud, 'Negative Sentiment', 2)

    # Maximum neutral sentiment
    max_neu_wordcloud = WordCloud(**wordcloud_params).generate(' '.join(max_neu_comments))
    display_wordcloud(max_neu_wordcloud, 'Neutral Sentiment', 3)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(expand=True, fill='both')

def clear_canvas():
    # Destroy the existing canvas
    for widget in root.winfo_children():
        if isinstance(widget, tk.Canvas):
            widget.destroy()

# Create the main window
root = tk.Tk()
root.title("Sentiment Analysis")
root.geometry("900x400")

# Create a label (title)
label = tk.Label(root, text="Sentiment Analysis of Palestine War", font=("Helvetica", 16))
label.pack(pady=20)

# Frame to hold buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Create buttons with styles
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 12))

button_vader = ttk.Button(button_frame, text="Generate Vader Results", command=generate_vader_results)
button_vader.pack(side=tk.LEFT, padx=5, expand=True, fill='both')

button_roberto = ttk.Button(button_frame, text="Generate Roberto Results", command=generate_roberto_results)
button_roberto.pack(side=tk.LEFT, padx=5, expand=True, fill='both')

button_compare = ttk.Button(button_frame, text="Compare Results", command=compare_results)
button_compare.pack(side=tk.LEFT, padx=5, expand=True, fill='both')

button_wordcount = ttk.Button(button_frame, text="Generate Wordcloud", command=generate_wordcount)
button_wordcount.pack(side=tk.LEFT, padx=5, expand=True, fill='both')

# Initialize the canvas for the first time
canvas = FigureCanvasTkAgg(plt.Figure(), master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(expand=True, fill='both')

# Create a single figure with 3 subplots in one row
fig = plt.figure(figsize=(18, 6))

# Set row and column weights
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Run the application
root.mainloop()
