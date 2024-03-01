from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quotes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote_text = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)

db.create_all()

def scrape_quotes():
    try:
        url = 'http://quotes.toscrape.com/'
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            quote = soup.find(class_='text').get_text()
            author = soup.find(class_='author').get_text()

            # Saving the scraped quote to the database
            new_quote = Quote(quote_text=quote, author=author)
            db.session.add(new_quote)
            db.session.commit()
            print('Quote saved to database:', quote)
        else:
            print('Failed to retrieve data - Status code:', response.status_code)
    except Exception as e:
        print('Error occurred:', e)

@app.route('/')
def home():
    return "Welcome to the Flask Web Scraping Application!"

@app.route('/scrape')
def scrape_and_save():
    scrape_quotes()
    return "Scraping done and data saved to database."

@app.route('/quotes')
def show_quotes():
    quotes = Quote.query.all()
    return jsonify([{'quote': q.quote_text, 'author': q.author} for q in quotes])

# Scheduler for automatic scraping
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(func=scrape_quotes, trigger='interval', minutes=30)
scheduler.start()

