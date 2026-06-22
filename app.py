from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import os

from config import Config
from models import db, ContactMessage

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow}

with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        app.logger.error(f"Init DB error: {e}")

@app.before_request
def ensure_db():
    try:
        db.create_all()
    except Exception:
        pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/a-propos')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        message = ContactMessage(
            nom=request.form.get('nom', ''),
            email=request.form.get('email', ''),
            telephone=request.form.get('telephone', ''),
            sujet=request.form.get('sujet', ''),
            message=request.form.get('message', '')
        )
        db.session.add(message)
        db.session.commit()
        flash('Votre message a été envoyé avec succès ! Nous vous répondrons dans les plus brefs délais.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
