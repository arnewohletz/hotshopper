"""Top-level package for hotshopper."""

__author__ = "Arne Wohletz"
__email__ = "arnewohletz@gmx.de"
__version__ = "1.0.0-rc"

import os
import secrets

from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

_app = Flask(__name__)

if os.environ.get("TEST_MODE") == "True":
    _app.testing = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    _app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
else:
    with Path(__file__).parent.resolve() / "recipes.db" as path:
        _app.config[
            "SQLALCHEMY_DATABASE_URI"] = \
            f"sqlite:///{path}?check_same_thread=False"
        _app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    _app.secret_key = secrets.token_hex()

# with Path(__file__).parent.resolve() / "recipes.db" as path:
#     print(f"Database path: {path}")
#     app.config[
#         "SQLALCHEMY_DATABASE_URI"] = \
#         f"sqlite:///{path}?check_same_thread=False"
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# app.secret_key = secrets.token_hex()

_db = SQLAlchemy(_app, session_options={"autoflush": False})
with _app.app_context():
    _db.create_all()
_app.app_context().push()

def get_app():
    # # app = Flask(__name__)
    # if test:
    #     app.testing = True
    #     app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    #     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    # else:
    #     with Path("hotshopper/recipes.db").resolve() as path:
    #         app.config[
    #             "SQLALCHEMY_DATABASE_URI"] = \
    #             f"sqlite:///{path}?check_same_thread=False"
    #         app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    #     app.secret_key = secrets.token_hex()
    # # db.init_app(app)
    # global db
    # db = SQLAlchemy(app, session_options={"autoflush": False})
    # db.create_all()
    # app.app_context().push()
    return _app

def get_db():
    return _db