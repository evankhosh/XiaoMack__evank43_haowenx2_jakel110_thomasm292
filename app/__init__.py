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

@app.route('/')
def root():
    if 'username' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('home'))

@app.route('/login')
def login():
    pass

@app.route('/register')
def register():
    pass

@app.route('/logout')
def logout():
    pass

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