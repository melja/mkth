from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from manage.auth import login_required
from manage.db import get_db
import zoneinfo

bp = Blueprint("user", __name__, url_prefix="/user")


def get_user(id):
    user = get_db().execute(
        "SELECT id, username, creation_date, access_enabled, "
        " password_last_updated, display_name, preferred_name, "
        " email, timezone, display_language "
        " FROM users WHERE id = ?",
        (id,)
    ).fetchone()

    if user is None:
        abort(404, f"User id {id} doesn't exist.")

    return user

@bp.route("/")
@login_required
def index():
    db = get_db()
    users = db.execute(
        "SELECT id, username, access_enabled, display_name, email, timezone, display_language"
        " FROM users"
        " ORDER BY username"
    ).fetchall()
    return render_template("user/list.html", users=users)

@bp.route("/profile")
@login_required
def profile():
    db = get_db()
    timezones=sorted(zoneinfo.available_timezones())
    return render_template("profile.html", timezones=timezones)

@bp.route("/search", methods=("POST",))
@login_required
def search():
    search = request.form.get("search", default="", type=str)
    db = get_db()
    users = db.execute(
        "SELECT id, username, access_enabled, display_name, email, timezone, display_language"
        " FROM users"
        " WHERE username LIKE :search"
        " OR display_name LIKE :search"
        " OR email LIKE :search"
        " ORDER BY username",
        { "search": "%"+search+"%" }
    ).fetchall()
    return render_template("user/search.html", users=users)


@bp.route("/<int:id>/edit", methods=("GET", "POST"))
@login_required
def edit(id):
    user = get_user(id)
    if request.method == "POST":
        username = request.form.get("username")
        display_name = request.form.get("display_name")
        email = request.form.get("email")
        timezone = request.form.get("timezone")
        display_language = request.form.get("display_language")
        error = None

        if not user:
            error = "Invalid identifier"

        if not username:
            error = "Username is required"

        if error is None:
            db = get_db()
            try:
                db.execute(
                    "UPDATE users SET username = ?, display_name = ?, email = ?, timezone = ?, display_language = ?"
                    " WHERE id = ?",
                    (username, display_name, email, timezone, display_language, id)
                )
                db.commit()
            except:
                error = f"Failed to update record"
        if error:    
            flash(error)
        return redirect(url_for("user.index"))
    return render_template("user/edit.html", user=user)

@bp.route("/<int:id>/disable", methods=("POST",))
@login_required
def disable(id):
    error = None
    user = get_user(id)

    if not user:
        error = "Invalid identifier"

    if not user["access_enabled"] == "Y":
        error = "User is not enabled"

    if error is None:
        db = get_db()
        try:
            db.execute(
                "UPDATE users SET access_enabled = 'N' WHERE id = ?",
                (id,)
            )
            db.commit()
            user = get_user(id)
        except:
            error = f"Failed to update record"
    if error:    
        print(error)
        flash(error)
    
    return render_template("user/search.html", users=[user])

@bp.route("/<int:id>/enable", methods=("POST",))
@login_required
def enable(id):
    user = get_user(id)
    error = None

    if not user:
        error = "Invalid identifier"

    if user["access_enabled"] == "Y":
        error = "User is already enabled"

    if error is None:
        db = get_db()
        try:
            db.execute(
                "UPDATE users SET access_enabled = 'Y' WHERE id = ?",
                (id,)
            )
            db.commit()
            user = get_user(id)
        except:
            error = f"Failed to update record"
    if error:    
        flash(error)
    return render_template("user/search.html", users=[user])
