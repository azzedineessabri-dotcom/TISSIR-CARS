from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, send_from_directory
from functools import wraps
import os
import secrets
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from sqlalchemy import extract

from config import Config
from models import db, Car, Reservation, ContactMessage, User, Setting

try:
    from cloudinary_storage import configurer_cloudinary, uploader_image, supprimer_image
except ImportError:
    configurer_cloudinary = lambda app: None
    uploader_image = lambda file, dossier='': (None, None)
    supprimer_image = lambda public_id: False

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
try:
    mail = Mail(app)
except Exception:
    mail = None
try:
    configurer_cloudinary(app)
except Exception:
    pass

def charger_parametres():
    mapping = {
        'company_name': 'COMPANY_NAME',
        'company_address': 'COMPANY_ADDRESS',
        'company_phone': 'COMPANY_PHONE',
        'company_phone2': 'COMPANY_PHONE2',
        'company_email': 'COMPANY_EMAIL',
        'company_hours_week': 'COMPANY_HOURS_WEEK',
        'company_hours_weekend': 'COMPANY_HOURS_WEEKEND',
        'company_facebook': 'COMPANY_FACEBOOK',
        'company_instagram': 'COMPANY_INSTAGRAM',
        'smtp_server': 'MAIL_SERVER',
        'smtp_port': 'MAIL_PORT',
        'smtp_username': 'MAIL_USERNAME',
        'smtp_password': 'MAIL_PASSWORD',
        'smtp_sender': 'MAIL_DEFAULT_SENDER',
        'admin_email': 'ADMIN_EMAIL',
        'whatsapp_number': 'WHATSAPP_NUMBER',
    }
    for key, config_key in mapping.items():
        val = Setting.get(key)
        if val:
            if config_key == 'MAIL_PORT':
                try:
                    app.config['MAIL_PORT'] = int(val)
                except ValueError:
                    pass
            else:
                app.config[config_key] = val
    if mail:
        try:
            mail.init_app(app)
        except Exception:
            pass

UPLOAD_FOLDER = '/tmp/uploads' if os.environ.get('VERCEL') else os.path.join(os.path.dirname(__file__), 'static', 'uploads')
try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
except Exception:
    pass

def save_car_image(file):
    if not file or file.filename == '':
        return None, None
    try:
        url, public_id = uploader_image(file)
        if url:
            return url, public_id
    except Exception:
        pass
    filename = secure_filename(file.filename)
    if not filename:
        return None, None
    name, ext = os.path.splitext(filename)
    filename = f"{name}_{secrets.token_hex(4)}{ext}"
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)
    return filename, None

def est_disponible(car_id, date_debut, date_fin):
    car = Car.query.get(car_id)
    if not car:
        return False
    count = Reservation.query.filter(
        Reservation.car_id == car_id,
        Reservation.statut != 'Annulée',
        Reservation.date_debut < date_fin,
        Reservation.date_fin > date_debut
    ).count()
    return count < car.quantity

def rester_disponible(car_id):
    now = datetime.now()
    car = Car.query.get(car_id)
    if not car:
        return 0
    count = Reservation.query.filter(
        Reservation.car_id == car_id,
        Reservation.statut != 'Annulée',
        Reservation.date_debut <= now,
        Reservation.date_fin >= now
    ).count()
    return max(0, car.quantity - count)

app.jinja_env.globals.update(rester_disponible=rester_disponible)

def generer_numero_reservation():
    ts = datetime.now().strftime('%y%m%d')
    dernier = Reservation.query.filter(Reservation.reservation_number.like(f'RES-{ts}%')).order_by(Reservation.id.desc()).first()
    if dernier:
        n = int(dernier.reservation_number.split('-')[-1]) + 1
    else:
        n = 1
    return f"RES-{ts}-{n:04d}"

with app.app_context():
    try:
        db.create_all()
        from sqlalchemy import text
        try:
            db.session.execute(text("ALTER TABLE reservation ALTER COLUMN statut TYPE VARCHAR(50)"))
            db.session.commit()
        except Exception:
            db.session.rollback()
        try:
            db.session.execute(text("ALTER TABLE car ADD COLUMN quantity INTEGER DEFAULT 1"))
            db.session.commit()
        except Exception:
            db.session.rollback()
        try:
            db.session.execute(text("UPDATE car SET quantity = 1 WHERE quantity IS NULL"))
            db.session.commit()
        except Exception:
            db.session.rollback()
        if Car.query.count() == 0:
            cars = [
                Car(name='Logan', brand='Dacia', category='Économique', transmission='Manuelle', fuel='Diesel', seats=5, price_per_day=300, quantity=3, image='clio_38860fad.jpg', description='Berline économique, idéale pour la ville. Faible consommation.'),
                Car(name='Clio', brand='Renault', category='Économique', transmission='Manuelle', fuel='Essence', seats=5, price_per_day=350, quantity=2, image='clio_38860fad.jpg', description='Citadine polyvalente, maniable et économique.'),
                Car(name='208', brand='Peugeot', category='Économique', transmission='Manuelle', fuel='Essence', seats=5, price_per_day=350, quantity=2, image='208_ef744d2f.jpg', description='Design moderne et agréable à conduire.'),
                Car(name='Golf', brand='Volkswagen', category='Économique', transmission='Automatique', fuel='Diesel', seats=5, price_per_day=400, quantity=2, image='8_cebe32fe.jpg', description='Référence du segment, confort et fiabilité.'),
                Car(name='Duster', brand='Dacia', category='SUV', transmission='Manuelle', fuel='Diesel', seats=5, price_per_day=500, quantity=3, image='Duster_dd636010.jpg', description='SUV robuste, parfait pour les routes marocaines.'),
                Car(name='Rav4', brand='Toyota', category='SUV', transmission='Automatique', fuel='Hybride', seats=5, price_per_day=700, quantity=2, image='Rav4_14cf1815.jpg', description='SUV hybride, économique et spacieux.'),
                Car(name='Hilux', brand='Toyota', category='SUV', transmission='Manuelle', fuel='Diesel', seats=5, price_per_day=650, quantity=2, image='Hilux_2f998dbe.jpg', description='Pick-up increvable, idéal pour les longs trajets.'),
                Car(name='Série 3', brand='BMW', category='Luxe', transmission='Automatique', fuel='Essence', seats=5, price_per_day=1200, quantity=1, image='Serie_3_8e2e4dbb.jpg', description='Berline de luxe, performance et élégance.'),
                Car(name='Classe C', brand='Mercedes', category='Luxe', transmission='Automatique', fuel='Diesel', seats=5, price_per_day=1400, quantity=1, image='Classe_C_f89fbe70.jpg', description='Luxe allemand, confort absolu.'),
                Car(name='A4', brand='Audi', category='Luxe', transmission='Automatique', fuel='Diesel', seats=5, price_per_day=1300, quantity=1, image='A4_ef1716c2.jpg', description='Élégance et technologie réunies.'),
            ]
            db.session.add_all(cars)
            db.session.commit()
        charger_parametres()
    except Exception as e:
        app.logger.error(f"Init DB error: {e}")

@app.before_request
def ensure_db():
    try:
        db.create_all()
    except Exception:
        pass

@app.errorhandler(Exception)
def handle_error(e):
    app.logger.error(f"Unhandled error: {e}")
    return "<h1>Erreur interne</h1><p>L'application rencontre un problème. Vérifiez les logs.</p>", 500

@app.route('/static/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/')
def index():
    try:
        cars = Car.query.all()
    except Exception:
        cars = []
    categories = ['Économique', 'SUV', 'Luxe']
    grouped = {c: [car for car in cars if car.category == c] for c in categories}
    grouped = {k: v for k, v in grouped.items() if v}
    return render_template('index.html', grouped=grouped)

@app.route('/catalogue')
def catalogue():
    category = request.args.get('category', '')
    transmission = request.args.get('transmission', '')
    fuel = request.args.get('fuel', '')
    query = Car.query
    if category:
        query = query.filter(Car.category == category)
    if transmission:
        query = query.filter(Car.transmission == transmission)
    if fuel:
        query = query.filter(Car.fuel == fuel)
    cars = query.all()
    categories = ['Économique', 'SUV', 'Luxe']
    grouped = {c: [car for car in cars if car.category == c] for c in categories}
    grouped = {k: v for k, v in grouped.items() if v}
    return render_template('catalog.html', grouped=grouped,
                         selected_category=category,
                         selected_transmission=transmission,
                         selected_fuel=fuel)

@app.route('/voiture/<int:car_id>')
def car_detail(car_id):
    car = Car.query.get_or_404(car_id)
    return render_template('car_detail.html', car=car)

@app.route('/reserver', methods=['GET', 'POST'])
def reserver():
    if request.method == 'POST':
        car_id = request.form.get('car_id')
        date_debut_str = request.form.get('date_debut')
        date_fin_str = request.form.get('date_fin')
        time_debut_str = request.form.get('time_debut')
        time_fin_str = request.form.get('time_fin')

        if not car_id or not date_debut_str or not date_fin_str:
            flash('Veuillez sélectionner une voiture et des dates.', 'error')
            return redirect(url_for('catalogue'))

        car = Car.query.get_or_404(car_id)

        if time_debut_str and time_fin_str:
            date_debut_str = f"{date_debut_str}T{time_debut_str}"
            date_fin_str = f"{date_fin_str}T{time_fin_str}"
        elif 'T' not in date_debut_str:
            date_debut_str += 'T10:00'
            date_fin_str += 'T10:00'

        a = secrets.randbelow(20) + 1
        b = secrets.randbelow(10) + 1
        session['captcha_answer'] = a + b

        date_debut = datetime.strptime(date_debut_str, '%Y-%m-%dT%H:%M')
        date_fin = datetime.strptime(date_fin_str, '%Y-%m-%dT%H:%M')
        if not est_disponible(car.id, date_debut, date_fin):
            flash('Ce véhicule n\'est pas disponible pour les dates sélectionnées.', 'error')
            return redirect(url_for('car_detail', car_id=car.id))
        duree = (date_fin - date_debut).days
        if duree < 1:
            duree = 1
        prix_total = duree * car.price_per_day

        return render_template('booking.html', car=car,
                             date_debut=date_debut_str,
                             date_fin=date_fin_str,
                             duree=duree,
                             prix_total=prix_total,
                             captcha_a=a, captcha_b=b)

    car_id = request.args.get('car_id')
    if car_id:
        return redirect(url_for('car_detail', car_id=car_id))
    return render_template('booking.html', car=None)

@app.route('/confirmer-reservation', methods=['POST'])
def confirmer_reservation():
    car_id = request.form.get('car_id')
    date_debut_str = request.form.get('date_debut')
    date_fin_str = request.form.get('date_fin')
    time_debut_str = request.form.get('time_debut')
    time_fin_str = request.form.get('time_fin')
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    email = request.form.get('email')
    telephone = request.form.get('telephone')
    captcha = request.form.get('captcha', '')
    expected = session.pop('captcha_answer', None)
    if expected is None or not captcha.isdigit() or int(captcha) != expected:
        flash('Réponse de sécurité incorrecte. Veuillez réessayer.', 'error')
        return redirect(url_for('catalogue'))

    car = Car.query.get_or_404(car_id)
    if time_debut_str and time_fin_str:
        date_debut_str = f"{date_debut_str}T{time_debut_str}"
        date_fin_str = f"{date_fin_str}T{time_fin_str}"
    elif 'T' not in date_debut_str:
        date_debut_str += 'T10:00'
        date_fin_str += 'T10:00'
    date_debut = datetime.strptime(date_debut_str, '%Y-%m-%dT%H:%M')
    date_fin = datetime.strptime(date_fin_str, '%Y-%m-%dT%H:%M')
    if not est_disponible(car.id, date_debut, date_fin):
        flash('Ce véhicule n\'est pas disponible pour les dates sélectionnées.', 'error')
        return redirect(url_for('catalogue'))
    duree = (date_fin - date_debut).days
    if duree < 1:
        duree = 1
    prix_total = duree * car.price_per_day
    numero = generer_numero_reservation()

    reservation = Reservation(
        reservation_number=numero,
        client_nom=nom,
        client_prenom=prenom,
        client_email=email,
        client_telephone=telephone,
        car_id=car.id,
        date_debut=date_debut,
        date_fin=date_fin,
        duree=duree,
        prix_total=prix_total,
        statut='En attente de confirmation'
    )
    db.session.add(reservation)
    db.session.commit()

    # Sauvegarde notification admin locale
    log_dir = '/tmp/mail_log' if os.environ.get('VERCEL') else os.path.join(os.path.dirname(__file__), 'mail_log')
    try:
        os.makedirs(log_dir, exist_ok=True)
    except Exception:
        pass
    admin_html = f"""<div style="font-family:sans-serif;max-width:600px;margin:0 auto">
        <div style="background:#1a2a4a;padding:20px;text-align:center">
            <h1 style="color:#1d6bf0;margin:0">{app.config.get('COMPANY_NAME', 'Sannad Tech')}</h1>
        </div>
        <div style="padding:30px;background:#f9f9f9">
            <h2 style="color:#1a2a4a">Nouvelle Réservation {numero}</h2>
            <h3 style="color:#1a2a4a;border-bottom:2px solid #1d6bf0;padding-bottom:5px">Client</h3>
            <p><strong>Nom:</strong> {nom} {prenom}<br>
            <strong>Email:</strong> {email}<br>
            <strong>Téléphone:</strong> {telephone}</p>
            <h3 style="color:#1a2a4a;border-bottom:2px solid #1d6bf0;padding-bottom:5px">Véhicule</h3>
            <p><strong>Voiture:</strong> {car.brand} {car.name}<br>
            <strong>Catégorie:</strong> {car.category}<br>
            <strong>Transmission:</strong> {car.transmission}, {car.fuel}</p>
            <h3 style="color:#1a2a4a;border-bottom:2px solid #1d6bf0;padding-bottom:5px">Location</h3>
            <p><strong>Du:</strong> {date_debut.strftime('%d/%m/%Y à %H:%M')}<br>
            <strong>Au:</strong> {date_fin.strftime('%d/%m/%Y à %H:%M')}<br>
            <strong>Durée:</strong> {duree} jours<br>
            <strong>Total:</strong> {prix_total:.0f} DH</p>
            <p style="background:#fef3c7;padding:10px;border-radius:5px"><strong>Statut:</strong> En attente de confirmation - Paiement sur place</p>
        </div></div>"""
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    try:
        with open(os.path.join(log_dir, f'admin_{numero}_{ts}.html'), 'w', encoding='utf-8') as f:
            f.write(admin_html)
    except Exception:
        pass

    # Notification admin par email si configuré
    try:
        if app.config.get('MAIL_USERNAME') and app.config.get('MAIL_PASSWORD') and app.config.get('ADMIN_EMAIL'):
            msg_admin = Message(
                subject=f"Nouvelle Réservation - {numero}",
                recipients=[app.config.get('ADMIN_EMAIL', app.config.get('MAIL_USERNAME'))],
                sender=app.config.get('MAIL_DEFAULT_SENDER', app.config.get('MAIL_USERNAME'))
            )
            msg_admin.html = admin_html
            mail.send(msg_admin)
    except Exception as e:
        app.logger.error(f"Erreur envoi mail admin: {e}")

    return render_template('confirmation.html', reservation=reservation, car=car)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        message = ContactMessage(
            nom=request.form.get('nom'),
            email=request.form.get('email'),
            telephone=request.form.get('telephone', ''),
            sujet=request.form.get('sujet'),
            message=request.form.get('message')
        )
        db.session.add(message)
        db.session.commit()

        try:
            if app.config.get('MAIL_USERNAME') and app.config.get('MAIL_PASSWORD'):
                msg = Message(
                    subject=f"Contact: {message.sujet} - {message.nom}",
                    recipients=[app.config.get('ADMIN_EMAIL', app.config.get('MAIL_USERNAME'))],
                    sender=app.config.get('MAIL_DEFAULT_SENDER', app.config.get('MAIL_USERNAME'))
                )
                msg.body = f"De: {message.nom} ({message.email})\nTel: {message.telephone}\n\n{message.message}"
                mail.send(msg)
        except Exception as e:
            app.logger.error(f"Erreur envoi mail contact: {e}")

        flash('Votre message a été envoyé avec succès !', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html')

@app.route('/api/cars')
def api_cars():
    cars = Car.query.all()
    return jsonify([{
        'id': c.id, 'name': c.name, 'brand': c.brand,
        'category': c.category, 'transmission': c.transmission,
        'fuel': c.fuel, 'seats': c.seats,
        'price_per_day': c.price_per_day, 'image': c.image,
        'description': c.description
    } for c in cars])

# ─── Admin ──────────────────────────────────────────────────────────
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == app.config.get('ADMIN_USERNAME', 'admin') and password == app.config.get('ADMIN_PASSWORD', 'admin123'):
            session['admin_logged_in'] = True
            session['admin_username'] = username
            session['admin_role'] = 'superadmin'
            return redirect(url_for('admin_dashboard'))

        user = User.query.filter_by(username=username, active=True).first()
        if user and user.check_password(password):
            session['admin_logged_in'] = True
            session['admin_username'] = user.username
            session['admin_user_id'] = user.id
            session['admin_role'] = user.role
            if user.force_password_change:
                return redirect(url_for('admin_change_password'))
            return redirect(url_for('admin_dashboard'))

        flash('Identifiants incorrects', 'error')
    return render_template('admin/login.html')

@app.route('/admin/mot-de-passe-oublie', methods=['GET', 'POST'])
def admin_forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        user = User.query.filter_by(email=email).first()
        if user:
            password = secrets.token_urlsafe(10)
            user.set_password(password)
            user.force_password_change = True
            db.session.commit()
            try:
                msg = Message(
                    subject='Nouveau mot de passe Sannad Tech',
                    recipients=[email],
                    sender=app.config['MAIL_DEFAULT_SENDER']
                )
                msg.body = f"""Bonjour {user.username},

Vous avez demandé un nouveau mot de passe pour votre compte administrateur Sannad Tech.

Nouveau mot de passe : {password}

Lien de connexion : {request.host_url}admin/login

Merci,
L'équipe Sannad Tech"""
                mail.send(msg)
                flash('Un nouveau mot de passe vous a été envoyé par email.', 'success')
            except Exception as e:
                app.logger.error(f"Erreur envoi nouveau mot de passe: {e}")
                flash("Impossible d'envoyer l'email. Vérifiez la configuration SMTP.", 'error')
        else:
            flash('Aucun compte trouvé avec cet email.', 'error')
        return redirect(url_for('admin_forgot_password'))
    return render_template('admin/forgot_password.html')

@app.route('/admin/changer-mot-de-passe', methods=['GET', 'POST'])
def admin_change_password():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    user_id = session.get('admin_user_id')
    user = User.query.get(user_id) if user_id else None
    if not user:
        session.pop('admin_logged_in', None)
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        nouveau = request.form.get('nouveau_password')
        confirmation = request.form.get('confirmation_password')
        if not nouveau or len(nouveau) < 4:
            flash('Le mot de passe doit contenir au moins 4 caractères.', 'error')
        elif nouveau != confirmation:
            flash('Les mots de passe ne correspondent pas.', 'error')
        else:
            user.set_password(nouveau)
            user.force_password_change = False
            db.session.commit()
            flash('Mot de passe modifié avec succès.', 'success')
            return redirect(url_for('admin_dashboard'))
    return render_template('admin/change_password.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin')
@admin_required
def admin_dashboard():
    total_cars = Car.query.count()
    total_reservations = Reservation.query.count()
    total_messages = ContactMessage.query.count()
    recent_reservations = Reservation.query.order_by(Reservation.date_reservation.desc()).limit(5).all()
    return render_template('admin/dashboard.html', total_cars=total_cars,
                         total_reservations=total_reservations,
                         total_messages=total_messages,
                         reservations=recent_reservations)

@app.route('/admin/cars')
@admin_required
def admin_cars():
    cars = Car.query.all()
    return render_template('admin/cars.html', cars=cars)

@app.route('/admin/cars/ajouter', methods=['GET', 'POST'])
@admin_required
def admin_car_add():
    if request.method == 'POST':
        image_path, image_public_id = save_car_image(request.files.get('image'))
        if not image_path:
            image_path = 'car-placeholder.jpg'
            image_public_id = None
        car = Car(
            name=request.form.get('name'),
            brand=request.form.get('brand'),
            category=request.form.get('category'),
            transmission=request.form.get('transmission'),
            fuel=request.form.get('fuel'),
            seats=int(request.form.get('seats', 5)),
            price_per_day=float(request.form.get('price_per_day', 0)),
            quantity=int(request.form.get('quantity', 1)),
            description=request.form.get('description', ''),
            available=request.form.get('available') == 'on',
            image=image_path,
            image_public_id=image_public_id or ''
        )
        db.session.add(car)
        db.session.commit()
        flash('Voiture ajoutée avec succès', 'success')
        return redirect(url_for('admin_cars'))
    return render_template('admin/car_form.html', car=None)

@app.route('/admin/cars/modifier/<int:car_id>', methods=['GET', 'POST'])
@admin_required
def admin_car_edit(car_id):
    car = Car.query.get_or_404(car_id)
    if request.method == 'POST':
        car.name = request.form.get('name')
        car.brand = request.form.get('brand')
        car.category = request.form.get('category')
        car.transmission = request.form.get('transmission')
        car.fuel = request.form.get('fuel')
        car.seats = int(request.form.get('seats', 5))
        car.price_per_day = float(request.form.get('price_per_day', 0))
        car.quantity = int(request.form.get('quantity', 1))
        car.description = request.form.get('description', '')
        car.available = request.form.get('available') == 'on'
        image_path, image_public_id = save_car_image(request.files.get('image'))
        if image_path:
            old_image = car.image
            old_public_id = car.image_public_id
            car.image = image_path
            car.image_public_id = image_public_id or ''
            if old_image and old_image != 'car-placeholder.jpg':
                if old_public_id:
                    supprimer_image(old_public_id)
                else:
                    chemin = os.path.join(UPLOAD_FOLDER, old_image)
                    if os.path.exists(chemin):
                        os.remove(chemin)
        db.session.commit()
        flash('Voiture modifiée avec succès', 'success')
        return redirect(url_for('admin_cars'))
    return render_template('admin/car_form.html', car=car)

@app.route('/admin/cars/supprimer/<int:car_id>', methods=['POST'])
@admin_required
def admin_car_delete(car_id):
    car = Car.query.get_or_404(car_id)
    if car.image and car.image != 'car-placeholder.jpg':
        if car.image_public_id:
            supprimer_image(car.image_public_id)
        else:
            chemin = os.path.join(UPLOAD_FOLDER, car.image)
            if os.path.exists(chemin):
                os.remove(chemin)
    db.session.delete(car)
    db.session.commit()
    flash('Voiture supprimée', 'success')
    return redirect(url_for('admin_cars'))

@app.route('/admin/reservations')
@admin_required
def admin_reservations():
    status = request.args.get('status', '')
    query = Reservation.query
    if status:
        query = query.filter(Reservation.statut == status)
    reservations = query.order_by(Reservation.date_reservation.desc()).all()
    return render_template('admin/reservations.html', reservations=reservations, selected_status=status)

def envoyer_email_reservation(reservation, statut):
    car = reservation.car
    log_dir = '/tmp/mail_log' if os.environ.get('VERCEL') else os.path.join(os.path.dirname(__file__), 'mail_log')
    try:
        os.makedirs(log_dir, exist_ok=True)
    except Exception:
        pass

    if statut == 'Confirmé':
        sujet = f"Réservation Confirmée - {reservation.reservation_number}"
        titre = "✓ Réservation Confirmée"
        intro = f"Votre réservation {reservation.reservation_number} est confirmée !"
        statut_badge = "Confirmé - Paiement sur place"
        bg = "#22c55e"
    elif statut == 'Annulée':
        sujet = f"Réservation Annulée - {reservation.reservation_number}"
        titre = "✗ Réservation Annulée"
        intro = f"Nous vous informons que votre réservation {reservation.reservation_number} a été annulée. Toutes nos excuses pour la gêne occasionnée. Nous restons à votre disposition pour toute information complémentaire."
        statut_badge = "Annulée"
        bg = "#ef4444"
    elif statut == 'Terminée':
        sujet = f"Réservation Terminée - {reservation.reservation_number}"
        titre = "✓ Réservation Terminée"
        intro = f"Nous vous remercions d'avoir choisi {app.config.get('COMPANY_NAME', 'Sannad Tech')} pour votre location. Votre réservation {reservation.reservation_number} est maintenant terminée. Au plaisir de vous accueillir de nouveau très prochainement."
        statut_badge = "Terminée"
        bg = "#1d6bf0"
    else:
        sujet = f"Mise à jour réservation {reservation.reservation_number}"
        titre = "Mise à Jour"
        intro = f"Votre réservation {reservation.reservation_number} a été mise à jour."
        statut_badge = statut
        bg = "#1d6bf0"

    company = app.config.get('COMPANY_NAME', 'Sannad Tech')
    html = f"""<div style="font-family:sans-serif;max-width:600px;margin:0 auto">
        <div style="background:#1a2a4a;padding:30px;text-align:center">
            <h1 style="color:{bg};margin:0">{titre}</h1>
            <p style="color:white;margin:5px 0 0;font-size:0.9rem">{company}</p>
        </div>
        <div style="padding:30px;background:#f9f9f9">
            <h2 style="color:#1a2a4a">Bonjour {reservation.client_prenom} !</h2>
            <p>{intro}</p>
            <div style="background:white;padding:15px;border-radius:8px;margin:20px 0;text-align:center">
                <p style="margin:0;font-size:0.95rem;color:#666">
                    <strong>N° {reservation.reservation_number}</strong> &nbsp;|&nbsp;
                    {car.brand} {car.name} &nbsp;|&nbsp;
                    {reservation.date_debut.strftime('%d/%m/%Y')} → {reservation.date_fin.strftime('%d/%m/%Y')} &nbsp;|&nbsp;
                    {reservation.duree}j &nbsp;|&nbsp;
                    <strong style="color:#1d6bf0;font-size:1.1rem">{reservation.prix_total:.0f} DH</strong>
                </p>
                <p style="margin:10px 0 0;font-size:0.85rem;background:#fef3c7;padding:5px 10px;border-radius:5px;display:inline-block"><strong>Statut:</strong> {statut_badge}</p>
            </div>
            <p style="margin-top:30px">Cordialement,<br><strong style="color:#0f2b5e">{app.config.get('COMPANY_NAME', 'Sannad Tech')}</strong></p>
            <p style="font-size:0.85rem;color:#999">{app.config.get('COMPANY_ADDRESS', '')} | {app.config.get('COMPANY_PHONE', '')}</p>
        </div></div>"""

    # Sauvegarde locale
    try:
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        fname = f"statut_{reservation.reservation_number}_{ts}.html"
        with open(os.path.join(log_dir, fname), 'w', encoding='utf-8') as f:
            f.write(html)
    except Exception:
        pass

    # Envoi SMTP
    smtp_envoye = False
    try:
        if app.config.get('MAIL_USERNAME') and app.config.get('MAIL_PASSWORD'):
            msg = Message(subject=sujet, recipients=[reservation.client_email], sender=app.config.get('MAIL_DEFAULT_SENDER', app.config.get('MAIL_USERNAME')))
            msg.html = html
            mail.send(msg)
            smtp_envoye = True
    except Exception as e:
        app.logger.error(f"Erreur envoi email statut: {e}")

    return smtp_envoye

@app.route('/admin/reservations/statut/<int:res_id>', methods=['POST'])
@admin_required
def admin_reservation_status(res_id):
    res = Reservation.query.get_or_404(res_id)
    nouveau_statut = request.form.get('statut', 'En attente de confirmation')
    ancien_statut = res.statut
    res.statut = nouveau_statut
    db.session.commit()

    if nouveau_statut != ancien_statut:
        envoye = envoyer_email_reservation(res, nouveau_statut)
        if envoye:
            flash(f'Statut mis à jour → {nouveau_statut}. Email envoyé au client.', 'success')
        else:
            flash(f'Statut mis à jour → {nouveau_statut}. Email sauvegardé (SMTP indisponible).', 'success')
    else:
        flash('Statut mis à jour', 'success')
    return redirect(url_for('admin_reservations'))

@app.route('/admin/reservations/email/<int:res_id>', methods=['POST'])
@admin_required
def admin_resend_email(res_id):
    res = Reservation.query.get_or_404(res_id)
    envoye = envoyer_email_reservation(res, res.statut)
    if envoye:
        flash(f'Email renvoyé à {res.client_email}', 'success')
    else:
        flash(f'Email sauvegardé (SMTP non configuré). '
              'Configurez SMTP dans Paramètres > Email pour envoyer des emails.', 'warning')
    return redirect(url_for('admin_reservations'))

@app.route('/admin/reservations/supprimer/<int:res_id>', methods=['POST'])
@admin_required
def admin_reservation_delete(res_id):
    res = Reservation.query.get_or_404(res_id)
    db.session.delete(res)
    db.session.commit()
    flash('Réservation supprimée', 'success')
    return redirect(url_for('admin_reservations'))

@app.route('/admin/messages')
@admin_required
def admin_messages():
    messages = ContactMessage.query.order_by(ContactMessage.date_envoi.desc()).all()
    return render_template('admin/messages.html', messages=messages)

@app.route('/admin/messages/lu/<int:msg_id>', methods=['POST'])
@admin_required
def admin_message_read(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    msg.lu = not msg.lu
    db.session.commit()
    return redirect(url_for('admin_messages'))

@app.route('/admin/messages/supprimer/<int:msg_id>', methods=['POST'])
@admin_required
def admin_message_delete(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    db.session.delete(msg)
    db.session.commit()
    flash('Message supprimé', 'success')
    return redirect(url_for('admin_messages'))

@app.route('/admin/email/test', methods=['POST'])
@admin_required
def admin_email_test():
    try:
        if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
            flash('SMTP non configuré. Remplissez MAIL_USERNAME et MAIL_PASSWORD dans le fichier .env', 'error')
            return redirect(url_for('admin_dashboard'))
        msg = Message(
            subject="Test Sannad Tech - Email configuration OK",
            recipients=[app.config['ADMIN_EMAIL']],
            sender=app.config['MAIL_DEFAULT_SENDER']
        )
        msg.html = "<h2>Test réussi</h2><p>Votre configuration email Sannad Tech fonctionne correctement.</p>"
        mail.send(msg)
        flash(f'Email de test envoyé avec succès à {app.config["ADMIN_EMAIL"]}', 'success')
    except Exception as e:
        flash(f'Erreur envoi email test: {e}', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/emails')
@admin_required
def admin_emails():
    log_dir = '/tmp/mail_log' if os.environ.get('VERCEL') else os.path.join(os.path.dirname(__file__), 'mail_log')
    files = []
    if os.path.exists(log_dir):
        for f in sorted(os.listdir(log_dir), reverse=True):
            if f.endswith('.html'):
                fpath = os.path.join(log_dir, f)
                files.append({'name': f, 'size': os.path.getsize(fpath),
                            'modified': datetime.fromtimestamp(os.path.getmtime(fpath)).strftime('%d/%m/%Y %H:%M')})
    return render_template('admin/emails.html', files=files)

@app.route('/admin/emails/<path:filename>')
@admin_required
def admin_email_view(filename):
    log_dir = '/tmp/mail_log' if os.environ.get('VERCEL') else os.path.join(os.path.dirname(__file__), 'mail_log')
    return send_from_directory(log_dir, filename)

@app.route('/admin/emails/supprimer-tous', methods=['POST'])
@admin_required
def admin_emails_delete_all():
    log_dir = '/tmp/mail_log' if os.environ.get('VERCEL') else os.path.join(os.path.dirname(__file__), 'mail_log')
    if os.path.exists(log_dir):
        for f in os.listdir(log_dir):
            if f.endswith('.html'):
                os.remove(os.path.join(log_dir, f))
    flash('Tous les emails logués ont été supprimés', 'success')
    return redirect(url_for('admin_emails'))

@app.route('/admin/settings', methods=['GET', 'POST'])
@admin_required
def admin_settings():
    if session.get('admin_role') == 'employe':
        flash('Accès refusé.', 'error')
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        champs = {
            'company_name': request.form.get('company_name', 'Sannad Tech'),
            'company_address': request.form.get('company_address', ''),
            'company_phone': request.form.get('company_phone', ''),
            'company_phone2': request.form.get('company_phone2', ''),
            'company_email': request.form.get('company_email', ''),
            'company_hours_week': request.form.get('company_hours_week', ''),
            'company_hours_weekend': request.form.get('company_hours_weekend', ''),
            'company_facebook': request.form.get('company_facebook', ''),
            'company_instagram': request.form.get('company_instagram', ''),
            'smtp_server': request.form.get('smtp_server', ''),
            'smtp_port': request.form.get('smtp_port', '587'),
            'smtp_username': request.form.get('smtp_username', ''),
            'smtp_password': request.form.get('smtp_password', ''),
            'smtp_sender': request.form.get('smtp_sender', ''),
            'admin_email': request.form.get('admin_email', ''),
            'whatsapp_number': request.form.get('whatsapp_number', '212600000000').replace(' ', '').replace('+', '').replace('-', ''),
        }
        for key, val in champs.items():
            Setting.set(key, val)
        charger_parametres()
        app.config['MAIL_SERVER'] = Setting.get('smtp_server', app.config.get('MAIL_SERVER', 'smtp.gmail.com'))
        app.config['MAIL_PORT'] = int(Setting.get('smtp_port', app.config.get('MAIL_PORT', 587)))
        app.config['MAIL_USERNAME'] = Setting.get('smtp_username', '')
        app.config['MAIL_PASSWORD'] = Setting.get('smtp_password', '')
        app.config['MAIL_DEFAULT_SENDER'] = Setting.get('smtp_sender', 'Sannad Tech <contact@sannadtech.ma>')
        app.config['ADMIN_EMAIL'] = Setting.get('admin_email', '')
        app.config['WHATSAPP_NUMBER'] = Setting.get('whatsapp_number', '212600000000').replace(' ', '').replace('+', '').replace('-', '')

        flash('Paramètres enregistrés avec succès', 'success')
        return redirect(url_for('admin_settings'))

    pre = lambda k, d: Setting.get(k, d)
    d = app.config
    return render_template('admin/settings.html',
        company_name=pre('company_name', d.get('COMPANY_NAME', 'Sannad Tech')),
        company_address=pre('company_address', d.get('COMPANY_ADDRESS', '123 Avenue Hassan II, Casablanca')),
        company_phone=pre('company_phone', d.get('COMPANY_PHONE', '+212 5XX-XXXXXX')),
        company_phone2=pre('company_phone2', d.get('COMPANY_PHONE2', '+212 6XX-XXXXXX')),
        company_email=pre('company_email', d.get('COMPANY_EMAIL', 'contact@sannadtech.ma')),
        company_hours_week=pre('company_hours_week', d.get('COMPANY_HOURS_WEEK', 'Lun - Sam : 08:00 - 20:00')),
        company_hours_weekend=pre('company_hours_weekend', d.get('COMPANY_HOURS_WEEKEND', 'Dimanche : 09:00 - 16:00')),
        company_facebook=pre('company_facebook', d.get('COMPANY_FACEBOOK', '')),
        company_instagram=pre('company_instagram', d.get('COMPANY_INSTAGRAM', '')),
        smtp_server=pre('smtp_server', d.get('MAIL_SERVER', 'smtp.gmail.com')),
        smtp_port=pre('smtp_port', str(d.get('MAIL_PORT', 587))),
        smtp_username=pre('smtp_username', d.get('MAIL_USERNAME', '')),
        smtp_password=pre('smtp_password', d.get('MAIL_PASSWORD', '')),
        smtp_sender=pre('smtp_sender', d.get('MAIL_DEFAULT_SENDER', 'Sannad Tech <contact@sannadtech.ma>')),
        admin_email=pre('admin_email', d.get('ADMIN_EMAIL', '')),
        whatsapp_number=pre('whatsapp_number', d.get('WHATSAPP_NUMBER', '212600000000')))

@app.route('/admin/users')
@admin_required
def admin_users():
    if session.get('admin_role') == 'employe':
        flash('Accès refusé.', 'error')
        return redirect(url_for('admin_dashboard'))
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/users/ajouter', methods=['GET', 'POST'])
@admin_required
def admin_user_add():
    if session.get('admin_role') == 'employe':
        flash('Accès refusé.', 'error')
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        role = request.form.get('role', 'admin')

        if User.query.filter_by(username=username).first():
            flash('Ce nom d\'utilisateur existe déjà', 'error')
            return render_template('admin/user_form.html', user=None)

        if User.query.filter_by(email=email).first():
            flash('Cet email existe déjà', 'error')
            return render_template('admin/user_form.html', user=None)

        user = User(username=username, email=email, role=role)
        if request.form.get('auto_password'):
            password = secrets.token_urlsafe(10)
            user.set_password(password)
            user.force_password_change = True
            db.session.add(user)
            db.session.commit()
            try:
                msg = Message(
                    subject='Vos identifiants Sannad Tech',
                    recipients=[email],
                    sender=app.config['MAIL_DEFAULT_SENDER']
                )
                msg.body = f"""Bonjour {username},

Votre compte administrateur Sannad Tech a été créé.

Identifiants de connexion :
  Utilisateur : {username}
  Mot de passe : {password}

Lien : {request.host_url}admin/login

Merci,
L'équipe Sannad Tech"""
                mail.send(msg)
                flash(f'Utilisateur ajouté. Mot de passe envoyé à {email}', 'success')
            except Exception as e:
                app.logger.error(f"Erreur envoi email nouveau mot de passe: {e}")
                flash(f'Utilisateur ajouté mais email non envoyé (SMTP non configuré) : {password}', 'warning')
        else:
            password = request.form.get('password')
            if not password:
                flash('Mot de passe requis', 'error')
                return render_template('admin/user_form.html', user=None)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Utilisateur ajouté avec succès', 'success')
        return redirect(url_for('admin_users'))

    return render_template('admin/user_form.html', user=None)

@app.route('/admin/users/modifier/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def admin_user_edit(user_id):
    if session.get('admin_role') == 'employe':
        flash('Accès refusé.', 'error')
        return redirect(url_for('admin_dashboard'))
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.role = request.form.get('role', 'admin')
        user.active = request.form.get('active') == 'on'
        password = request.form.get('password')
        if password:
            user.set_password(password)
        db.session.commit()
        flash('Utilisateur modifié avec succès', 'success')
        return redirect(url_for('admin_users'))

    return render_template('admin/user_form.html', user=user)

@app.route('/admin/users/supprimer/<int:user_id>', methods=['POST'])
@admin_required
def admin_user_delete(user_id):
    if session.get('admin_role') == 'employe':
        flash('Accès refusé.', 'error')
        return redirect(url_for('admin_dashboard'))
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Utilisateur supprimé', 'success')
    return redirect(url_for('admin_users'))

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
