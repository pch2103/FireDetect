import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    NEXT_SERVER = os.environ.get('NEXT_SERVER') or 'localhost'
    NEXT_PORT = os.environ.get('NEXT_PORT') or 8000
