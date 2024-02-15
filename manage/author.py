from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from manage.auth import login_required
from manage.db import get_db

bp = Blueprint("author", __name__, url_prefix="/author")

@bp.route("/")
@login_required
def index():
    db = get_db()
    authors = db.execute(
        "SELECT id, display_name"
        " FROM authors"
        " ORDER BY display_name"
    ).fetchall()
    return render_template("author/list.html", authors=authors)

@bp.route("/search", methods=("POST",))
@login_required
def search():
    search = request.form.get("search", default="", type=str)
    db = get_db()
    authors = db.execute(
        "SELECT id, display_name"
        " FROM authors"
        " WHERE display_name LIKE ?"
        " ORDER BY display_name",
        ("%"+search+"%",)
    ).fetchall()
    return render_template("author/search.html", authors=authors)


def get_author(id):
    author = get_db().execute(
        "SELECT id, display_name, creation_date, last_updated"
        " FROM authors WHERE id = ?",
        (id,)
    ).fetchone()

    if author is None:
        abort(404, f"Author id {id} doesn't exist.")

    return author

@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        name = request.form.get("name")
        error = None

        if not name:
            error = "Name is required"

        if error is None:
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO authors (display_name)"
                    " VALUES (?)",
                    (name,)
                )
                db.commit()
            except db.IntegrityError:
                error = f"Author {name} already exists"
        if error:    
            flash(error)
        return redirect(url_for("author.index"))
    return render_template("author/create.html")

@bp.route("/<int:id>/edit", methods=("GET", "POST"))
@login_required
def edit(id):
    author = get_author(id)
    if request.method == "POST":
        name = request.form.get("name")
        error = None

        if not author:
            error = "Invalid identifier"

        if not name:
            error = "Name is required"

        if error is None:
            db = get_db()
            try:
                db.execute(
                    "UPDATE authors SET display_name = ? WHERE id = ?",
                    (name, id)
                )
                db.commit()
            except:
                error = f"Failed to update record"
        if error:    
            flash(error)
        return redirect(url_for("author.index"))
    return render_template("author/edit.html", author=author)

@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    author = get_author(id)
    db = get_db()
    db.execute("DELETE FROM authors WHERE id = ?", (author["id"],))
    db.commit()
    return redirect(url_for("author.index"))
