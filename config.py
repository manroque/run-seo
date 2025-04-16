import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "chave-secreta")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/runseo.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = "filesystem"
