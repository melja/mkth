import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import login_user, LoginManager, UserMixin
from . import db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'mkth0_manage.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile(os.path.join(app.instance_path, 'config.py'), silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #login_manager = LoginManager()
    #login_manager.init_app(app)

    @app.errorhandler(404)
    def not_found(error):
        return render_template('error.html'), 404
        
    def validate_login(username, password):
        if username == "admin":
            return True
        return False

    sourcelist = [
            ("Serious Research Text", "Dr Oswald Busyson, MD"),
            ("Current Health Claims, Volume 13", "Martha Marysdottir-Winthorpe"),
            ("Prominent Science Today", "Editors")
        ]
    
    authorlist = [ 
            "Dr Oswald Busyson, MD",
            "Martha Marysdottir-Winthorpe",
            "Editors",
            "Harrold Hairychest, DO"
    ]
      
    @app.route("/increment", methods=["POST"])
    def increment():
        if "username" not in session:
            return f'Count: 0'
        if "count" in session:
            count = session["count"] + 1
        else:
            count = 0
        session["count"] = count
        return f'Count: {count}'

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/login/", methods=["GET", "POST"])
    def login():
        tourl = request.args.get('next')
        if not tourl:
            tourl = url_for("home")
        print(f"tourl { tourl }")
        if request.method == "GET":
            return render_template("login.html", error=False, tourl=tourl)
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            tourl = request.form["tourl"]
            if validate_login(username, password):
                flash('You were successfully logged in')
                session["username"] = username
                return redirect(tourl)
            session["username"] = None
            app.logger.warning(f"Failed login for username \"{ username }\"")
            flash('Invalid username or password')
            return render_template("login.html", error=True)
        
    @app.route("/logout/", methods=["GET"])
    def logout():
            session.pop('username', None)
            return redirect(url_for("login"))
        
    @app.route("/home/", methods=["GET"])
    def home():
        if "username" not in session:
            return redirect(url_for("login", next=url_for("home")))
        if "count" in session:
            count = session["count"]
        else:
            count = 0
        return render_template("home.html", count=count)

    @app.route("/sources/", methods=["GET", "POST"])
    def sources():
        if "username" not in session:
            return redirect(url_for("login", next=url_for("sources")))
        if request.method=="GET":
            return render_template("sources.html", sources=sourcelist)
        sourcelist.append((request.form["title"],request.form["authors"]))
        return redirect(url_for("sources"))
        

    @app.route("/authors/", methods=["GET", "POST"])
    def authors():
        if "username" not in session:
            return redirect(url_for("login", next=url_for("authors")))
        if request.method=="GET":
            return render_template("authors.html", authors=authorlist)
        authorlist.append(request.form["name"])
        return redirect(url_for("authors"))

    db.init_app(app)

    return app