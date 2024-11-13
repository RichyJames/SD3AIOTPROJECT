from flask import Flask
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient('localhost', 27017)


db = client.flask_database
todos = db.todos

@app.route('/')
def home():
    return "Flask app is running and connected to MongoDB!"

if __name__ == "__main__":
    app.run(debug=True)