"""Top-level package for hotshopper."""

__author__ = "Arne Wohletz"
__email__ = "arnewohletz@gmx.de"
__version__ = "0.2.0"

import secrets
from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)


def create_app(test=False):
    # app = Flask(__name__)
    if test:
        app.testing = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    else:
        with Path("hotshopper/recipes.db").resolve() as path:
            app.config[
                "SQLALCHEMY_DATABASE_URI"] = \
                f"sqlite:///{path}?check_same_thread=False"
            app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
        app.secret_key = secrets.token_hex()
    # db.init_app(app)
    db.create_all()
    app.app_context().push()
    return app


# with Path("hotshopper/recipes.db").resolve() as path:
#     app.config[
#         "SQLALCHEMY_DATABASE_URI"] = \
#         f"sqlite:///{path}?check_same_thread=False"
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# app.secret_key = secrets.token_hex()
# db = SQLAlchemy(app)
