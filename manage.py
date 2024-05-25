from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_postgres_uri'
db = SQLAlchemy(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
