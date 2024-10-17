# Import necessary libraries
from flask import Flask, request, render_template, send_file
from bs4 import BeautifulSoup
import re
import requests
from googleapiclient import discovery
import pandas as pd
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

app = Flask(__name__)

# Function to extract video ID from YouTube video URL using web scraping
def extract_video_id(video_url):
    try:
        response = requests.get(video_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        meta_tag = soup.find("meta", itemprop="videoId")
        if meta_tag:
            video_id = meta_tag.get("content")
            return video_id
        else:
            video_id = video_url.split("v=")[-1]
            return video_id
    except Exception as e:
        print("Error:", e)
        return None

# Function to fetch comments using Google API
def fetch_comments(video_id):
    try:
        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = "AIzaSyBKoen8XSnu502ilPfN3Dcagsiggetj2Is"
        
        youtube = discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
                maxResults=1000
        )
        response = request.execute()

        comments = []

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            text = comment['textDisplay']
            sentiment_score = TextBlob(text).sentiment.polarity
            # Assign sentiment label based on sentiment score
            if sentiment_score > 0.2:
                sentiment_label = 'Positive'
            elif sentiment_score < -0.2:
                sentiment_label = 'Negative'
            else:
                sentiment_label = 'Neutral'
            comments.append({'text': text, 'sentiment_score': sentiment_score, 'sentiment_label': sentiment_label})

        df = pd.DataFrame(comments)
        return df
    except Exception as e:
        print("Error:", e)
        return None

# Function to generate word cloud
def generate_word_cloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    return img_base64

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for analyzing YouTube video comments
@app.route('/analyze', methods=['POST'])
def analyze():
    video_url = request.form['url']
    video_id = extract_video_id(video_url)
    if video_id:
        comments_df = fetch_comments(video_id)
        if comments_df is not None:
            wordcloud_img = generate_word_cloud(' '.join(comments_df['text']))
            return render_template('result.html', 
                                    wordcloud_img=wordcloud_img,
                                    comments=comments_df.to_html(),
                                    video_url=video_url)
        else:
            return "Failed to fetch comments."
    else:
        return "Video ID extraction failed."

# Route for searching keyword in YouTube video comments
@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    video_url = request.form['video_url']
    video_id = extract_video_id(video_url)
    if video_id:
        comments_df = fetch_comments(video_id)
        if comments_df is not None:
            keyword_frequency = comments_df['text'].str.lower().str.count(keyword.lower()).sum()
            top_positive_comments = list(comments_df.nlargest(5, 'sentiment_score')['text'])
            top_negative_comments = list(comments_df.nsmallest(5, 'sentiment_score')['text'])
            wordcloud_img = generate_word_cloud(' '.join(comments_df['text']))

            # Perform classification
            X = comments_df['text']
            y = comments_df['sentiment_label']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            vectorizer = TfidfVectorizer()
            X_train = vectorizer.fit_transform(X_train)
            X_test = vectorizer.transform(X_test)
            classifier = LogisticRegression(max_iter=1000)
            classifier.fit(X_train, y_train)
            y_pred = classifier.predict(X_test)

            # Generate classification report
            report = classification_report(y_test, y_pred)

            return render_template('result.html', 
                                    wordcloud_img=wordcloud_img,
                                    keyword=keyword,
                                    keyword_frequency=keyword_frequency,
                                    top_positive_comments=top_positive_comments,
                                    top_negative_comments=top_negative_comments,
                                    comments=comments_df.to_html(),
                                    classification_report=report,
                                    video_url=video_url)
        else:
            return "Failed to fetch comments."
    else:
        return "Video ID extraction failed."

if __name__ == '__main__':
    app.run(debug=True)
