import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read environment variables from .env file
DEV_DB_USER_NAME = os.getenv('DEV_DB_USER')
DEV_DB_USER_PASS = os.getenv('DEV_DB_PASS')
DEV_DB_HOST = os.getenv('DEV_DB_HOST')
DEV_DB_PORT = os.getenv('DEV_DB_PORT')
DEV_DB_NAME = os.getenv('DEV_DB_NAME')

DB_USER_NAME = os.getenv('DB_USER')
DB_USER_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY')
    RECAPTCHA_VERIFY_URL = os.getenv('RECAPTCHA_VERIFY_URL')
    RECAPTCHA_SITE_KEY = os.getenv('RECAPTCHA_SITE_KEY')
    RECAPTCHA_SECRET_KEY = os.getenv('RECAPTCHA_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(BaseConfig):
    ENV = "development"
    DEBUG = True
    charset = 'utf8mb4'
    SQLALCHEMY_DATABASE_URI = f'mysql://{DEV_DB_USER_NAME}:{DEV_DB_USER_PASS}@{DEV_DB_HOST}:{DEV_DB_PORT}/{DEV_DB_NAME}?charset=utf8mb4'


class ProductionConfig(BaseConfig):
    ENV = "production"
    DEBUG = False
    charset = 'utf8mb4'
    SQLALCHEMY_DATABASE_URI = f'mysql://{DB_USER_NAME}:{DB_USER_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4'
