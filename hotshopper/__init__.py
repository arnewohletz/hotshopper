"""Top-level package for hotshopper."""

__author__ = "Arne Wohletz"
__email__ = "arnewohletz@gmx.de"
__version__ = "0.2.0"

import secrets
from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
db = SQLAlchemy()


def create_app(test=False):
    app = Flask(__name__)
    if test:
        # app = Flask(__name__)
        app.testing = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        # db.init_app(app)
        # app.app_context().push()
    else:
        with Path("hotshopper/recipes.db").resolve() as path:
            app.config[
                "SQLALCHEMY_DATABASE_URI"] = \
                f"sqlite:///{path}?check_same_thread=False"
            app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
        app.secret_key = secrets.token_hex()
    db.init_app(app)
    app.app_context().push()
    return app
# create_app = lambda: Flask(__name__)


# with Path("hotshopper/recipes.db").resolve() as path:
#     app.config[
#         "SQLALCHEMY_DATABASE_URI"] = \
#         f"sqlite:///{path}?check_same_thread=False"
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# app.secret_key = secrets.token_hex()
# db = SQLAlchemy(app)
