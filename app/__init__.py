'''
    XiaoMack: Evan Khosh, Thomas Mackey, Haowen Xiao, Jake Liu
    P02: Makers Makin' It, Act I
    1-16-26
'''
import sqlite3, json#, requests
from flask import Flask, render_template, session, request, redirect, url_for
from data import *
from random import shuffle

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
    if 'username' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        data = request.form

        # store username and password as a variable
        username = data['username'].strip()
        password = data['password'].strip()

        # render login page if username or password box is empty
        if not username or not password:
            return render_template('login.html', error="No username or password inputted")

        #search user table for password from a certain username
        try:
            auth(username, password)
            session['username'] = username
            return redirect(url_for("home"))

        except ValueError as e:
            return render_template("login.html", error=e)

    return render_template('login.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        data = request.form

        username = data['username'].strip()
        password = data['password'].strip()

        # reload page if no username or password was entered
        if not username or not password:
            return render_template('login.html', error="No username or password inputted")

        try:
            register_user(username, password)
            session['username'] = username
            return redirect(url_for("home"))
        
        except ValueError as e:
            return render_template("register.html", error=e)

    return render_template("register.html")

@app.route('/logout')
def logout():
    session.pop('username', None)

    return redirect(url_for("root"))

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        data = request.form
        print(data['title'])

        if 'title' in data:
            session['title'] = data['title']
            add_points(session['username'], len(get_flashcard_content(data['title'])))

            return redirect(url_for("flashcards"))

    print(get_flashcards())

    return render_template(
        'home.html',
        flashcards=get_flashcards()
    )

@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    print(session["username"])

    if request.method == 'POST':
        data = request.form

        # form list of card tuples
        cards = []
        num_cards = int(data['create_btn'])
        for i in range(1, num_cards + 1):
            front = data[f"front_{i}"]
            back = data[f"back_{i}"]
            cards.append((front, back))

        try:
            new_flashcard(data['title'], cards, session['username'])
            
        except ValueError as e:
            return render_tempate('create.html', error=e)
        
        return redirect(url_for('home'))

    return render_template('create.html')

@app.route('/flashcards', methods=['GET', 'POST'])
def flashcards():
    if 'username' not in session:
        return redirect(url_for('login'))

    if 'title' not in session:
        return redirect(url_for('home'))

    creator = get_field("flashcards", "title", session["title"], "creator")
    flashcards = get_flashcard_content(session["title"])
    print(flashcards)

    return render_template(
        'flashcards.html',
        title=session["title"],
        creator=creator,
        flashcards=flashcards
    )

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if 'title' not in session:
        return redirect(url_for('home'))

    creator = get_field("flashcards", "title", session["title"], "creator")
    flashcards = get_flashcard_content(session["title"])

    if request.method == "POST":
        data = request.get_json()
        print(data.get("q"))
        print(data.get("ans"))

    return render_template(
        'quiz.html',
        title=session['title'],
        creator=creator,
        flashcards=flashcards
    )

@app.route('/matchpair', methods=['GET', 'POST'])
def matchpair():
    if 'username' not in session:
        return redirect(url_for('login'))

    if 'title' not in session:
        return redirect(url_for('home'))

    creator = get_field("flashcards", "title", session["title"], "creator")
    flashcards = get_flashcard_content(session["title"])

    fronts, backs = zip(*flashcards)
    fronts = list(fronts)
    backs = list(backs)
    shuffle(backs)
    shuffle(fronts)
    shuffled_flashcards = list(zip(fronts, backs))

    return render_template(
        'match_pair.html',
        title=session["title"],
        creator=creator,
        flashcards=flashcards,
        shuffled_flashcards=shuffled_flashcards
    )

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    error = None

    if request.method == 'POST':
        data = request.form
        action = data.get('action')

        try:
            if action == 'change_username':
                new_username = data.get('new_username', '').strip()
                change_username(username, new_username)
                session['username'] = new_username
                username = new_username

            elif action == 'change_password':
                old_pass = data.get('old_password', '').strip()
                new_pass = data.get('new_password', '').strip()
                change_password(username, old_pass, new_pass)

            elif action == 'review':
                title = data.get('title', '').strip()
                if title:
                    session['title'] = title
                    return redirect(url_for('flashcards'))

        except ValueError as e:
            error = str(e)

    return render_template(
        'profile.html',
        username=username,
        points=get_points(username),
        flashcards=get_user_flashcards(username),
        error=error
    )

if __name__ == "__main__":
    app.debug = True
    app.run()
