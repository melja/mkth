import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import login_user, LoginManager, UserMixin

count = 0

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'mkth0.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    sourcelist = [
            ("Serious Research Text", "Dr Oswald Busyson, MD"),
            ("Current Health Claims, Volume 13", "Martha Marysdottir-Winthorpe"),
            ("Prominent Science Today", "Editors")
        ]
    
    def increment_count(session):
        if "count" in session:
            count = session["count"] + 1
        else:
            count = session["count"] = 0
        session["count"] = count
        return count

    @app.route("/")
    def index():
        if "count" in session:
            count = session["count"]
        else:
            count = 0
        return render_template("index.html", count=count)
    
    @app.route("/increment", methods=["POST"])
    def increment():
        count = increment_count(session)
        return f'<button id="counter" hx-post="/increment" hx-swap="outerHTML">Count: {count}</button>'

    @app.route("/login/", methods=["GET", "POST"])
    def login():
        if request.method == "GET":
            return render_template("login.html", error=False)
        if request.method == "POST":
            if request.form["username"] != "admin":
                return render_template("login.html", error=True)
            return redirect(url_for("index"))
        
    @app.route("/sources/", methods=["GET", "POST"])
    def sources():
        if request.method=="GET":
            return render_template("sources.html", sources=sourcelist)
        sourcelist.append((request.form["title"],request.form["authors"]))
        return redirect(url_for("sources"))
        
    import db
    db.init_app(app)

    return app

app = create_app()