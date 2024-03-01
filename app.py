
from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Flask Web Scraping Application!"

@app.route('/scrape')
def scrape():
    # Simple web scraping logic
    url = 'http://quotes.toscrape.com/'  # A simple webpage for scraping quotes
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extracting the first quote from the page
    quote = soup.find(class_='text').get_text()
    author = soup.find(class_='author').get_text()

    # Returning the scraped data as JSON
    return jsonify({'quote': quote, 'author': author})

if __name__ == '__main__':
    app.run(debug=True)
