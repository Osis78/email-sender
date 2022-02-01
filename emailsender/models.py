from emailsender.config import db
from sqlalchemy.orm import backref

# Create DB models

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(12), unique=True, nullable=False)
    last_connexion = db.Column(db.Time, unique=False, nullable=True)

    def __repr__(self):
        return '<User %r>' % self.email

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    sender = db.Column(db.String(255), unique=False, nullable=False)
    subject = db.Column(db.String(255), unique=False, nullable=True)
    content = db.Column(db.Text, unique=False, nullable=True)
    a_envoyer = db.Column(db.Integer, unique=False, nullable=False)
    filters = db.Column(db.String(255), unique=False, nullable=True)
    contacts = db.Column(db.Text, unique=False, nullable=True)
    sent = db.Column(db.Integer, unique=False, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('campaigns', lazy=True))

    def __repr__(self):
        return '<Campaign %r>' % self.name