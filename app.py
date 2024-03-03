
from flask import Flask, jsonify, request, render_template, url_for
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

def scrape_quotes(url='http://quotes.toscrape.com/'):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            quote = soup.find(class_='text').get_text()
            author = soup.find(class_='author').get_text()

            new_quote = Quote(quote_text=quote, author=author)
            db.session.add(new_quote)
            db.session.commit()
            return {'quote': quote, 'author': author}
        else:
            return {'error': 'Failed to retrieve data - Status code: {}'.format(response.status_code)}
    except Exception as e:
        return {'error': 'An error occurred: {}'.format(e)}

@app.route('/')
def home():
    quotes = Quote.query.all()
    return render_template('index.html', quotes=quotes)

@app.route('/scrape', methods=['POST'])
def scrape_and_save():
    url = request.form.get('url', 'http://quotes.toscrape.com/')
    result = scrape_quotes(url)
    if 'error' not in result:
        return jsonify(result)
    else:
        return jsonify(result), 500

@app.route('/quotes')
def show_quotes():
    quotes = Quote.query.all()
    return jsonify([{'quote': q.quote_text, 'author': q.author} for q in quotes])

# Scheduler for automatic scraping
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(func=scrape_quotes, trigger='interval', minutes=30)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run(debug=True)
