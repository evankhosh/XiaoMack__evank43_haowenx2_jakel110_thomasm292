'''
    XiaoMack: Evan Khosh, Thomas Mackey, Haowen Xiao, Jake Liu
    P02: Makers Makin' It, Act I
    1-16-26
'''
import sqlite3, json, requests
from flask import Flask, render_template, session, request, redirect, url_for
from data import *

app = Flask(__name__)

app.secret_key = "key"
DB_FILE = "data.db"

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
        try:
            auth(username, password)
            session["username"] = username
            return redirect(url_for("home"))
        except ValueError as E:
            return render_template("login.html", error=E)

    return render_template('login.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username').strip().lower()
        password = request.form.get('password').strip()

        # reload page if no username or password was entered
        try:
            register_user(username, password)
            session['username'] = username
            return redirect(url_for("home"))
        except ValueError as E:
            return render_template("register.html", error=E)

    return render_template("register.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for("root"))

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get("title")

        # form list of card tuples
        cards = []
        num_cards = int(request.form.get("create_btn"))
        for i in range(1, num_cards):
            front = request.form.get(f"front_{i}")
            back = request.form.get(f"back_{i}")
            cards.append((front, back))

        user = session["username"]

        new_flashcard(title, cards, user)

    return render_template('create.html')

@app.route('/flashcards', methods=['GET', 'POST'])
def flashcards():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('flashcards.html') 

if __name__ == "__main__":
    app.debug = True
    app.run()
