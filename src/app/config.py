from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv('/../.env')

# O MAX_CONTENT_LENGTH da o tamanho maximo de arquivos


class Config(object):
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@localhost/{os.getenv('DB_DATABASE')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 64 * 1000 * 1000
    UPLOAD_FOLDER = r'public\storage'