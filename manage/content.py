from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from manage.auth import login_required
from manage.db import get_db

bp = Blueprint('content', __name__, url_prefix='/content')

@bp.route("/authors", methods=["GET", "POST"])
@login_required
def authors():
    db = get_db()
    if request.method=="POST":
        name = request.form["name"]
        error = None

        if not name:
            error = "Name is required"

        if error is None:
            db = get_db()
            try:
                db.execute(
                    'INSERT INTO authors (name)'
                    ' VALUES (?)',
                    (name,)
                )
                db.commit()
            except db.IntegrityError:
                error = f"Author {name} already exists"
        if error:    
            flash(error)
        return redirect(url_for('content.authors'))

    authors = db.execute(
        'SELECT name'
        ' FROM authors'
        ' ORDER BY name'
    ).fetchall()
    return render_template('content/authors.html', authors=authors)
