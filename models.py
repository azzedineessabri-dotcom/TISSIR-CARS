from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    transmission = db.Column(db.String(20), nullable=False)
    fuel = db.Column(db.String(20), nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    price_per_day = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(500), nullable=False, default='car-placeholder.jpg')
    image_public_id = db.Column(db.String(200), default='')
    available = db.Column(db.Boolean, default=True)
    quantity = db.Column(db.Integer, default=1)
    description = db.Column(db.Text, default='')

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reservation_number = db.Column(db.String(20), unique=True, nullable=False)
    client_nom = db.Column(db.String(100), nullable=False)
    client_prenom = db.Column(db.String(100), nullable=False)
    client_email = db.Column(db.String(120), nullable=False)
    client_telephone = db.Column(db.String(20), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    date_debut = db.Column(db.DateTime, nullable=False)
    date_fin = db.Column(db.DateTime, nullable=False)
    duree = db.Column(db.Integer, nullable=False)
    prix_total = db.Column(db.Float, nullable=False)
    statut = db.Column(db.String(50), default='En attente')
    date_reservation = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text, default='')

    car = db.relationship('Car', backref='reservations')

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telephone = db.Column(db.String(20), default='')
    sujet = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_envoi = db.Column(db.DateTime, default=datetime.utcnow)
    lu = db.Column(db.Boolean, default=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='admin')
    active = db.Column(db.Boolean, default=True)
    force_password_change = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, default='')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def get(cls, key, default=''):
        s = cls.query.filter_by(key=key).first()
        return s.value if s else default

    @classmethod
    def set(cls, key, value):
        s = cls.query.filter_by(key=key).first()
        if s:
            s.value = value
            s.updated_at = datetime.utcnow()
        else:
            s = cls(key=key, value=value)
            db.session.add(s)
        db.session.commit()
        return s
