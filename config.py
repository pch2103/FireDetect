import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    UPLOAD_EXTENSIONS = ['.mp3', '.mp4', '.png', '.jpg', '.jpeg', '.gif', '.mkv', '.mpg', '.avi', '.mov', '.wmv']
    UPLOAD_PATH = os.environ.get('UPLOAD_PATH') or 'uploads/'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    NEXT_SERVER = os.environ.get('NEXT_SERVER') or '127.0.0.1'
    NEXT_PORT = os.environ.get('NEXT_PORT') or 8000
    MODEL_PATH = os.environ.get('MODEL_PATH') or None
