from flask import Flask, render_template
import requests
import json
import schedule
import time

app = Flask(__name__)

# Variable to store the latest news data
latest_news = []

def fetch_news():
    global latest_news
    api_key = 'ba562d1933bd35f20de59b6de4388f24'  # Replace with your actual API key
    api_url = 'https://gnews.io/api/v4/top-headlines'

    params = {'token': api_key, 'country': 'us'}
    response = requests.get(api_url, params=params)
    data = json.loads(response.text)

    latest_news = data.get('articles', [])

def update_news_periodically():
    # Schedule the fetch_news function to run every hour
    schedule.every().hour.do(fetch_news)

    # Run the scheduler in the background
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the background task to update news periodically
if __name__ == '__main__':
    # Start the background task in a separate thread
    import threading
    threading.Thread(target=update_news_periodically).start()

    # Run the Flask app
    app.run(debug=True)

@app.route('/')
def home():
    # Use the latest_news variable to display news on the site
    return render_template('index.html', articles=latest_news)
