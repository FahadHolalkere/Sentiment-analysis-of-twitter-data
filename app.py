from flask import Flask, render_template, jsonify, request
from wordcloud import WordCloud
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pickle
import subprocess
from threading import Lock

from pro import execute_selenium_script

app = Flask(__name__)
lock = Lock()

def plot_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

from wordcloud import WordCloud
from PIL import Image
from io import BytesIO
import base64

def generate_wordcloud(text):
    if not text:
        return None

    wordcloud = WordCloud(width=800, height=400, background_color='black', max_words=100).generate(text)

    image = wordcloud.to_image()

    img_buffer = BytesIO()
    image.save(img_buffer, format='PNG')
    img_buffer.seek(0)

    img_b64 = base64.b64encode(img_buffer.read()).decode('utf-8')

    return img_b64

def generate_wordclouds(df):
     # Check if 'Comments' column exists in the DataFrame
    if 'Comments' not in df.columns:
        return None, None, None

    # Separate comments based on sentiment
    positive_comments = ' '.join(df[df['pos'] > df[['neg', 'neu']].max(axis=1)]['Comments'].tolist())
    neutral_comments = ' '.join(df[df['neu'] > df[['pos', 'neg']].max(axis=1)]['Comments'].tolist())
    negative_comments = ' '.join(df[df['neg'] > df[['pos', 'neu']].max(axis=1)]['Comments'].tolist())

    # Generate WordClouds for each sentiment
    positive_b64 = generate_wordcloud(positive_comments)
    neutral_b64 = generate_wordcloud(neutral_comments)
    negative_b64 = generate_wordcloud(negative_comments)

    return positive_b64, neutral_b64, negative_b64

from datetime import datetime

def convert_date(date_str):
   # Ensure that date_str is a string
    if isinstance(date_str, float):
        date_str = str(date_str)

    date_str = date_str.strip()  # Remove leading and trailing whitespace
    date_str = date_str.strip('"')  # Remove quotes if present

    try:
        date_obj = datetime.strptime(date_str, '%b %d, %Y')
    except ValueError:
        # Handle invalid date format
        return None

    # Format the datetime object to dd-mm-yyyy format
    formatted_date = date_obj.strftime('%d-%m-%Y')
    
    return formatted_date

def generate_line_graph(df):
    df['Unnamed: 1'] = pd.to_datetime(df['Unnamed: 1'], errors='coerce')
    
    # Check for missing values in numerical columns and fill them
    numerical_columns = ['neg', 'neu', 'pos']
    df[numerical_columns] = df[numerical_columns].fillna(0)  
    
    # Convert numerical columns to numeric data type
    df[numerical_columns] = df[numerical_columns].astype(float)

    # Group the DataFrame by date and calculate the mean value
    df_grouped = df.groupby(df['Unnamed: 1'].dt.date).mean()

    # Plot the line graph
    plt.figure(figsize=(10, 6))
    plt.plot(df_grouped.index, mean_sentiment_roberta, marker='o', linestyle='-')
    plt.xlabel('Date')
    plt.ylabel('Mean Value')
    plt.title('Line Graph')
    plt.xticks(rotation=45)
    plt.grid(True)

    # Convert the plot to base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    return img_base64

@app.route('/getDate')
def getDate():
    df = pd.read_csv('tweet2.csv')
    # Generate the line graph
    line_graph_base64 = generate_line_graph(df)

    return render_template('graph.html', line_graph_base64=line_graph_base64)

@app.route('/graph')
def graph():
    return render_template('graph.html')

def clear_canvas():
    plt.clf()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        topic = request.form['topic']
        execute_selenium_script(topic)
        return f'Topic "{topic}" submitted successfully!'

@app.route('/analyze', methods=['POST'])
def analyze():
    with lock:
        label_text = "Comparison"
    
        subprocess.run(["python", "Vader.py"])
        with open('exported_data.pkl', 'rb') as file:
            df_vader = pickle.load(file)

        df_roberta = pd.read_csv('excel/tweet2.csv')
        clear_canvas()

        sentiment_counts_vader = df_vader['sentiment'].value_counts()
        mean_sentiment_roberta = df_roberta[['neg', 'neu', 'pos']].mean()

        fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(10, 4))

        axs[0].pie(sentiment_counts_vader, labels=sentiment_counts_vader.index, autopct='%1.1f%%', startangle=140, colors=['red', 'yellow', 'green'])
        axs[0].set_title('Vader')

        axs[1].pie(mean_sentiment_roberta, labels=['Negative', 'Neutral', 'Positive'], autopct='%1.1f%%', startangle=140, colors=['red', 'yellow', 'green'])
        axs[1].set_title('Roberta')

        positive_b64, neutral_b64, negative_b64 = generate_wordclouds(df_roberta)

        plt.tight_layout()

        canvas_b64 = plot_to_base64(fig)

        return render_template('index.html', label_text=label_text, canvas_b64=canvas_b64, 
                            positive_b64=positive_b64, neutral_b64=neutral_b64, negative_b64=negative_b64)
    

if __name__ == '__main__':
    app.run(debug=True)
