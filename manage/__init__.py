import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import login_user, LoginManager, UserMixin

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

    @app.route("/")
    def index():
        return render_template("index.html")
        
    from . import db
    db.init_app(app)

    from . import user
    app.register_blueprint(user.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import content
    app.register_blueprint(content.bp)

    from . import author
    app.register_blueprint(author.bp)

    from . import source
    app.register_blueprint(source.bp)

    return app