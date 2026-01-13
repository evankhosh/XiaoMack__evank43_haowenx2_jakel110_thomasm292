'''
    XiaoMack: Evan Khosh, Thomas Mackey, Haowen Xiao, Jake Liu
    P02: Makers Makin' It, Act I
    1-16-26
'''
import sqlite3, json, requests
from flask import Flask, render_template, session, request, redirect, url_for

app = Flask(__name__)

app.secret_key = "key"
DB_FILE = "data.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()


db.commit()
db.close()

@app.route("/", methods=['GET', 'POST'])
def root():
    if 'username' in session:
        return redirect(url_for("home"))

    return redirect(url_for("login"))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # store username and password as a variable
        username = request.form.get('username').strip().lower()
        password = request.form.get('password').strip()

        # render login page if username or password box is empty
        if not username or not password:
            return render_template('login.html', error="No username or password inputted")

        #search user table for password from a certain username
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        account = c.execute("SELECT password FROM users WHERE name = ?", (username,)).fetchone()
        db.close()

        #if there is no account then reload page
        if account is None:
            return render_template("login.html", error="Username or password is incorrect")

        # check if password is correct, if not then reload page
        if account[0] != password:
            return render_template("login.html", error="Username or password is incorrect")

        # if password is correct redirect home
        session["username"] = username
        return redirect(url_for("home"))

    return render_template('login.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username').strip().lower()
        password = request.form.get('password').strip()

        # reload page if no username or password was entered
        if not username or not password:
            return render_template("register.html", error="No username or password inputted")

        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        # check if username already exists and reload page if it does
        exists = c.execute("SELECT 1 FROM users WHERE name = ?", (username,)).fetchone()
        if exists:
            db.close()
            return render_template("register.html", error="Username already exists")

        db.commit()
        db.close()

        session['username'] = username
        return redirect(url_for("home"))
    return render_template("register.html")

@app.route('/logout')
def logout():
    session.pop('username', None)

@app.route('/home', methods=['GET', 'POST'])
def home_page():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/review')
def review_page():
    pass

if __name__ == "__main__":
    app.debug = True
    app.run()
