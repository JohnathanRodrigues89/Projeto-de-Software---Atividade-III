import os

SECRET_KEY = os.environ.get("SECRET_KEY", "troque-esta-chave-em-producao")
SQLALCHEMY_TRACK_MODIFICATIONS = False
