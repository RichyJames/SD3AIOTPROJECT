from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient('localhost', 27017)

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')



db = client.flask_database
todos = db.todos

@app.route('/')
def home():
    return "Flask app is running and it is connected to MongoDB"

if __name__ == "__main__":
    app.run(debug=True)