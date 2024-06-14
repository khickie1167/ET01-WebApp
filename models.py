from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    date_added = db.Column(db.DateTime, default=db.func.current_timestamp())
