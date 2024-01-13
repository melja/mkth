from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_user, LoginManager, UserMixin

app = Flask(__name__)

sourcelist = [
        ("Serious Research Text", "Dr Oswald Busyson, MD"),
        ("Current Health Claims, Volume 13", "Martha Marysdottir-Winthorpe"),
        ("Prominent Science Today", "Editors")
    ]

@app.route("/")
def index():
    return render_template("index.html")

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
    