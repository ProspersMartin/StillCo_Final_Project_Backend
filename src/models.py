from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Client(db.Model):
    client_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)


    def __repr__(self):
        return '<Client %r>' % self.email

    def serialize(self):
        return {
            "Client ID": self.client_id,
            "name": self.name,
            "email": self.email,
            "password": self.password
        }