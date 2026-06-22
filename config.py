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
        SQLALCHEMY_DATABASE_URI = 'sqlite:///sannadtech.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    COMPANY_NAME = 'Sannad Tech'
    COMPANY_SLOGAN = 'Innovation digitale au service de votre croissance'
    COMPANY_EMAIL = 'contact@sannadtech.ma'
    COMPANY_PHONE = '+212 5XX-XXXXXX'
    COMPANY_ADDRESS = 'Béni Mellal, Maroc'
