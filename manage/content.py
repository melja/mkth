from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from manage.auth import login_required
from manage.db import get_db

bp = Blueprint('content', __name__, url_prefix='/content')

@bp.route("/", methods=["GET"])
@login_required
def content():
    return render_template('content/content.html')

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
        'SELECT id, name'
        ' FROM authors'
        ' ORDER BY name'
    ).fetchall()
    return render_template('content/authors.html', authors=authors)

# def get_author(id):
#     author = get_db().execute(
#         'SELECT a.id, a.name, a.creation_date'
#         ' FROM authors a WHERE a.id = ?',
#         (id,)
#     ).fetchone()

#     if author is None:
#         abort(404, f"Author id {id} doesn't exist.")

#     return author

@bp.route('/delete_author/<int:id>', methods=('POST',))
@login_required
def delete_author(id):
    # author = get_author(id)
    db = get_db()
    db.execute('DELETE FROM authors WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('content.authors'))#, author=author)