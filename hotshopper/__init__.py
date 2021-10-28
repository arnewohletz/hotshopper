"""Top-level package for hotshopper."""

__author__ = "Arne Wohletz"
__email__ = "arnewohletz@gmx.de"
__version__ = "0.2.0"

import secrets
from pathlib import Path

from flask import (Flask)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

with Path("hotshopper/recipes.db").resolve() as path:
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{path}"
app.secret_key = secrets.token_hex()
db = SQLAlchemy(app)
