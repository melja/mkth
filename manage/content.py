from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from manage.auth import login_required
from manage.db import get_db

bp = Blueprint("content", __name__, url_prefix="/content")

types = {"author":"Authors","source":"Sources"}

@bp.route("/", methods=["GET"])
@login_required
def index():
    global types
    return render_template("content/index.html", types=types)

@bp.route("/none", methods=["GET"])
@login_required
def none():
    return render_template("content/none.html")

@bp.route("/<string:type>", methods=["GET"])
@login_required
def content(type):
    global types
    if type not in types:
        type = None
    return render_template("content/index.html", types=types, type=type)

