import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

    DATABASE_URL = os.environ.get('DATABASE_URL', '')
    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace('postgres://', 'postgresql://')
        SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_pre_ping': True,
            'pool_recycle': 300,
            'connect_args': {'sslmode': 'require'},
        }
    elif os.environ.get('VERCEL'):
        SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/db.sqlite'
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///car_rental.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'Sannad Tech <contact@sannadtech.ma>')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@locauto.ma')

    WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER', '212600000000')
    WHATSAPP_LINK = f'https://wa.me/{WHATSAPP_NUMBER}'
    WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER', '212600000000')

    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')

    COMPANY_NAME = os.environ.get('COMPANY_NAME', 'Sannad Tech')
    COMPANY_ADDRESS = os.environ.get('COMPANY_ADDRESS', 'Béni Mellal, Maroc')
    COMPANY_PHONE = os.environ.get('COMPANY_PHONE', '+212 5XX-XXXXXX')
    COMPANY_PHONE2 = os.environ.get('COMPANY_PHONE2', '+212 6XX-XXXXXX')
    COMPANY_EMAIL = os.environ.get('COMPANY_EMAIL', 'contact@sannadtech.ma')
    COMPANY_HOURS_WEEK = os.environ.get('COMPANY_HOURS_WEEK', 'Lun - Sam : 08:00 - 20:00')
    COMPANY_HOURS_WEEKEND = os.environ.get('COMPANY_HOURS_WEEKEND', 'Dimanche : 09:00 - 16:00')
    COMPANY_FACEBOOK = os.environ.get('COMPANY_FACEBOOK', '')
    COMPANY_INSTAGRAM = os.environ.get('COMPANY_INSTAGRAM', '')

    CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME', '')
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY', '')
    CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET', '')
