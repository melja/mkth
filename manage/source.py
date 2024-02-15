from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from manage.auth import login_required
from manage.db import get_db

bp = Blueprint("source", __name__, url_prefix="/source")

@bp.route("/")
@login_required
def index():
    db = get_db()
    sources = db.execute(
        "SELECT s.id, s.title, a.display_name AS author_name"
        " FROM sources AS s"
        " INNER JOIN authors as a ON s.authorid = a.id"
        " ORDER BY s.title"
    ).fetchall()
    return render_template("source/list.html", sources=sources)


@bp.route("/search", methods=("POST",))
@login_required
def search():
    search = request.form.get("search", default="", type=str)
    db = get_db()
    sources = db.execute(
        "SELECT s.id, s.title, a.display_name AS author_name"
        " FROM sources AS s"
        " INNER JOIN authors as a ON s.authorid = a.id"
        " WHERE s.title LIKE :search"
        " OR a.display_name LIKE :search"
        " ORDER BY s.title",
        { "search": "%"+search+"%" }
    ).fetchall()
    return render_template("source/search.html", sources=sources)


def get_source(id):
    source = get_db().execute(
        "SELECT s.id, s.title, s.creation_date, s.authorid"
        " FROM sources s WHERE s.id = ?",
        (id,)
    ).fetchone()

    if source is None:
        abort(404, f"Source id {id} doesn't exist.")

    return source

@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form.get("title")
        authorid = request.form.get("authorid")
        error = None

        if not title:
            error = "Title is required"
        if not authorid:
            error = "Author is required"

        if error is None:
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO sources (title, authorid)"
                    " VALUES (?, ?)",
                    (title, authorid)
                )
                db.commit()
            except db.IntegrityError:
                error = f"Title {title} already exists"
        if error:    
            flash(error)
        return redirect(url_for("source.index"))
    db = get_db()
    authors = db.execute(
        "SELECT id, display_name"
        " FROM authors"
        " ORDER BY display_name"
    ).fetchall()
    return render_template("source/create.html", authors=authors)

@bp.route("/<int:id>/edit", methods=("GET", "POST"))
@login_required
def edit(id):
    source = get_source(id)
    if request.method == "POST":
        title = request.form.get("title")
        authorid = request.form.get("authorid")
        error = None

        if not source:
            error = "Invalid identifier"

        if not title:
            error = "Name is required"
        if not authorid:
            error = "Author is required"

        if error is None:
            db = get_db()
            try:
                db.execute(
                    "UPDATE sources SET title = ?, authorid = ? WHERE id = ?",
                    (title, authorid, id)
                )
                db.commit()
            except:
                error = f"Failed to update record"
        if error:    
            flash(error)
        return redirect(url_for("source.index"))
    authors = get_db().execute(
        "SELECT id, display_name"
        " FROM authors"
        " ORDER BY display_name"
    ).fetchall()
    return render_template("source/edit.html", source=source, authors=authors)

@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    source = get_source(id)
    db = get_db()
    db.execute("DELETE FROM sources WHERE id = ?", (source["id"],))
    db.commit()
    return redirect(url_for("source.index"))
