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
from loguru import logger

# Intra-package imports

# import to make models visible to create_all() if database is not existing
# WARNING: creating an empty DB currently makes hotshopper unusable
from hotshopper.model import Base


# _app = None
# _db = None

_db = SQLAlchemy(model_class=Base,
                 session_options={"autoflush": False})


def create_application():
    # global _app, _db
    app = Flask(__name__)
    if os.environ.get("TEST_MODE", "False") == "True":
        logger.info("Create Flask app in test mode")
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    else:
        logger.info("Create Flask app")
        path = Path(__file__).parent.resolve() / "recipes.db"
        app.config["SQLALCHEMY_DATABASE_URI"] = \
            f"sqlite:///{path}?check_same_thread=False"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
        app.secret_key = secrets.token_hex()

        # if not path.exists():
        #     _db = _create_database()
        # else:
        #     _db = SQLAlchemy(model_class=Base,
        #                      session_options={"autoflush": False})
    # _db = SQLAlchemy(model_class=Base,
    #                  session_options={"autoflush": False})
    _db.init_app(app)
    with app.app_context():
        logger.info("Initializing database")
        _db.create_all()
    app.app_context().push()

    logger.info("Flask app initialized")
    return app


_app = create_application()

# def _create_database():
#     db = SQLAlchemy(model_class=Base,
#                     session_options={"autoflush": False})
#     db.create_all()
#     return db


def get_app():
    return _app


def get_db():
    return _db


# create_application()
