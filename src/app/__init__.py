from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from app.config import Config

class Base(DeclarativeBase):
    pass

app = Flask(__name__)
app.config.from_object(Config)
#db = SQLAlchemy(app)
db = SQLAlchemy(model_class=Base)
db.init_app(app)

from app import routes