"""Top-level package for hotshopper."""

__author__ = "Arne Wohletz"
__email__ = "arnewohletz@gmx.de"
__version__ = "1.0.0-rc"

import os
import secrets

from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import fontawesomefree

app = Flask(__name__)
# db = None
# db = SQLAlchemy(app, session_options={"autoflush": False})

if os.environ.get('TEST_MODE', False) is True:
    app.testing = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
else:
    with Path(__file__).parent.resolve() / "recipes.db" as path:
        app.config[
            "SQLALCHEMY_DATABASE_URI"] = \
            f"sqlite:///{path}?check_same_thread=False"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.secret_key = secrets.token_hex()

# with Path(__file__).parent.resolve() / "recipes.db" as path:
#     print(f"Database path: {path}")
#     app.config[
#         "SQLALCHEMY_DATABASE_URI"] = \
#         f"sqlite:///{path}?check_same_thread=False"
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# app.secret_key = secrets.token_hex()

db = SQLAlchemy(app, session_options={"autoflush": False})
with app.app_context():
    db.create_all()
app.app_context().push()

def create_app(test=False):
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
    return app

# with Path("hotshopper/recipes.db").resolve() as path:
#     app.config[
#         "SQLALCHEMY_DATABASE_URI"] = \
#         f"sqlite:///{path}?check_same_thread=False"
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# app.secret_key = secrets.token_hex()
# db = SQLAlchemy(app)
