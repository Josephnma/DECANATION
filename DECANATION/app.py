import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request,redirect, url_for, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, render_template, redirect, url_for

from flask import Flask, render_template

from flask_socketio import SocketIO, emit, send

from flask_socketio import send, emit


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

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

@app.route("/chat", methods=["POST", "GET"])
def chat():
    return render_template("chat.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/Tch_stk")
def Tch_stk():
    return render_template("Tch_stk.html")

@app.route("/jobportal")
def jobportal():
    return render_template("jobportal.html")

@app.route("/webinar")
def webinar():
    return render_template("webinar.html")

@app.route("/", methods=["GET", "POST"])
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
        return redirect("/index")

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
# req_search = search.query.filter_by(req_no=query)

@app.route("/learning")
def learning():
    return render_template("learning.html")

@app.route("/node", methods=["POST", "GET"])
def node():
    if request.method == "POST":
        message = request.form["message"]
        body = request.form["body"]
        return render_template("node.html", message=message, body=body)
    return render_template("node.html")

@app.route("/community")
def community():
    return render_template("community.html")

@app.route("/create", methods= ['POST', 'GET'])
def create():
    if request.method == 'POST':
        query = request.form['query']
        query2 = request.form['query2']
        return render_template("view.html", query = query, query2 = query2)
    return render_template("create.html")

@app.route("/view")
def view():
    return render_template("view.html")

@app.route("/nodethread")
def nodethread():
    return render_template("nodethread.html")

@app.route("/javathread")
def javathread():
    return render_template("javathread.html")

@app.route("/dotnetthread")
def dotnetthread():
    return render_template("dotnetthread.html")

@app.route("/golangthread")
def golangthread():
    return render_template("golangthread.html")

@app.route("/pythonthread")
def pythonthread():
    return render_template("pythonthread.html")

@app.route("/jobthread")
def jobthread():
    return render_template("jobthread.html")
    # query = request.args['search']

    #req_search = search.query.filter_by(req_no=query)


@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

@socketio.on('message')
def handle_message(message):
    send(message)

@socketio.on('json')
def handle_json(json):
    send(json, json=True)

@socketio.on('my event')

def handle_my_custom_event(json):
    emit('my response', json)

def ack():
    print('message was received!')

@socketio.on('my event')
def handle_my_custom_event(json):
    emit('my response', json, callback=ack)

@socketio.on('my event')
def handle_my_custom_event(data):
    emit('my response', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)




#return render_template("index.html")

