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
