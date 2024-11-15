from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
db = SQLAlchemy(app)


db = client.flask_database
todos = db.todos

@app.route('/')
def home():
    return "Flask app is running and it is connected to MongoDB"

if __name__ == "__main__":
    app.run(debug=True)