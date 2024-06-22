"""Top-level package for hotshopper."""

__author__ = "Arne Wohletz"
__email__ = "arnewohletz@gmx.de"
__version__ = "1.0.0-rc"

# Standard library imports
import os
import secrets
from pathlib import Path

# Third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Intra-package imports

# import to make models visible to create_all() if database is not existing
# WARNING: creating an empty DB currently makes hotshopper unusable
from hotshopper.model import *


_app = None
_db = None


def create_application():
    global _app, _db
    _app = Flask(__name__)
    if os.environ.get("TEST_MODE", "False") == "True":
        _app.config.update({"TESTING": True})
        _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        _app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    else:
        path = Path(__file__).parent.resolve() / "recipes.db"
        _app.config["SQLALCHEMY_DATABASE_URI"] = \
            f"sqlite:///{path}?check_same_thread=False"
        _app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
        _app.secret_key = secrets.token_hex()

    _db = SQLAlchemy(model_class=Base,
                     session_options={"autoflush": False})

    _db.init_app(_app)
    with _app.app_context():
        _db.create_all()
    _app.app_context().push()


def get_app():
    return _app


def get_db():
    return _db


create_application()
