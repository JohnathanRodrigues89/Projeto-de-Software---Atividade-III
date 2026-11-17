import os
from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "troque-esta-chave-em-producao"),
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            "DATABASE_URL",
            f"sqlite:///{Path(app.instance_path) / 'refugio_literario.db'}",
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    csrf.init_app(app)

    from app import models  # noqa: F401
    from app.routes import bp
    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

    return app
