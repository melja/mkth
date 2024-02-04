from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from manage.auth import login_required
from manage.db import get_db

bp = Blueprint("content", __name__, url_prefix="/content")

types = {"user":"Users","author":"Authors","source":"Sources"}

@bp.route("/", defaults={'type': None}, methods=["GET"])
@bp.route("/<string:type>", methods=["GET"])
@login_required
def index(type):
    global types
    if type not in types:
        if type:
            flash(f"Content type {type} not found")
        return redirect(url_for("content.index", type=list(types.keys())[0]))
    return render_template("content.html", types=types, type=type)

