import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request,redirect, url_for, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
# app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

from helpers import apology, login_required

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///decanation.db")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT id,hash,username FROM user WHERE username = ?", request.form.get("username"))
        print(rows)
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match", 400)

        check = db.execute("SELECT username FROM user WHERE username=?", request.form.get("username"))
        if len(check) > 0:
            return apology("username not available", 400)

        db.execute("INSERT INTO user (username, hash) VALUES(?, ?)", request.form.get(
            "username"), generate_password_hash(request.form.get("password")))

        return redirect("/")

    return render_template("register.html")

@app.route('/nodejs')
def nodejs():
    return render_template('nodejs.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/creat')
def creat():
    return render_template('creat.html')



@app.route('/ruby')
def ruby():
    return render_template('ruby.html')

@app.route('/golang')
def golang():
    return render_template('golang.html')

@app.route('/java')
def java():
    return render_template('java.html')

@app.route('/python')
def python():
    return render_template('python.html')

@app.route('/interview')
def interview():
    return render_template('interview.html')

@app.route('/likes')
def likes():
    return render_template('/like.html')

@app.route('/view')
def view():
    return render_template('/view.html')

@app.route('/noderesource')
def noderesource():
    return render_template('/noderesource.html')

@app.route('/golangresource')
def golangresource():
    return render_template('/golangresource.html')

@app.route('/pythonresource')
def pythonresource():
    return render_template('/pythonresource.html')

@app.route('/javaresource')
def javaresource():
    return render_template('/javaresource.html')

@app.route('/cresource')
def cresource():
    return render_template('/cresource.html')

#search
@app.route('/search', methods=["POST","GET"])  # 'GET' is the default method, you don't need to mention it explicitly
def search():
    # query = request.args['search']
    query = request.form.get("search").lower()  # try this instead
    if query == "login":
        return render_template("login.html")
    elif query == "register":
        return render_template("register.html")
    else:
        return "page not found"
    req_search = search.query.filter_by(req_no=query)


@app.route("/", methods=['POST', 'GET'])
def result():

    if request.method == 'POST':
       query = request.form['query']
       query2 = request.form['query2']
    #    response = MyService.retrieve_response(query)
       return render_template("view.html", query = query, query2 = query2)
    #return render_template("view.html")
if __name__ == "__main__":
    app.run()








