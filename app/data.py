import sqlite3   #enable control of an sqlite database
import secrets  # used to generate ids
import hashlib   #for consistent hashes


#=============================MAKE=TABLES=============================#

# make the database tables we need if they don't already exist

# user_info
def create_user_info():

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS user_info (
            username TEXT PRIMARY KEY NOT NULL,
            password TEXT NOT NULL,
            points INTEGER,
            flashcards TEXT
        )"""
    )

    db.commit()
    db.close()


# flashcards
def create_flashcards():

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS flashcards (
            title TEXT NOT NULL,
            creator TEXT NOT NULL,
            card INTEGER NOT NULL,
            front TEXT NOT NULL,
            back TEXT NOT NULL
        )"""
    )

    db.commit()
    db.close()


#=============================USERINFO=============================#


#----------USERINFO-ACCESSORS----------#


def get_points(username):
    return get_field('user_info', 'username', username, 'points')


def get_user_flashcards(username):
    # titles are stored as text; split the string (delimiter = %SPLIT%)
    # cut the first item, which is 'None'
    return get_field('user_info', 'username', username, 'flashcards').split('%SPLIT%')


#----------USERINFO-MUTATORS----------#


# adds a new user's data to user table
def register_user(username, password):

    if user_exists(username):
        raise ValueError("Username already exists")

    if password == "":
        raise ValueError("You must enter a non-empty password")

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    password = password.encode('utf-8')
    password = str(hashlib.sha256(password).hexdigest())

    command = 'INSERT INTO user_info VALUES (?, ?, NULL, NULL)'
    vars = (username, password)
    c.execute(command, vars)

    db.commit()
    db.close()

    return "success"


def change_username(old_username, new_username):

    if user_exists(new_username):
        raise ValueError("Username already exists")

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # update stuff associated with old username
    command = 'UPDATE flashcards SET creator = ? WHERE creator_username = ?'
    vars = (new_username, old_username)
    c.execute(command, vars)

    command = 'UPDATE user_info SET username = ? WHERE username = ?'
    vars = (new_username, old_username)
    c.execute(command, vars)

    db.commit()
    db.close()

    return "success"


def change_password(username, old_pass, new_pass):

    if not auth(username, old_pass):
        raise ValueError("Incorrect old password")

    if new_pass == "":
        raise ValueError("New password must be non-empty")

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    new_pass = new_pass.encode('utf-8')
    new_pass = str(hashlib.sha256(new_pass).hexdigest())

    command = 'UPDATE user_info SET password = ? WHERE username = ?'
    vars =(new_pass, username)
    c.execute(command, vars)

    db.commit()
    db.close()

    return "success"


def add_points(username, points):

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # get current list of stuff in the row
    points = get_field('user_info', 'username', username, 'points') + points

    command = 'UPDATE user_info SET points = ? WHERE username = ?'
    vars = (points, username)
    c.execute(command, vars)

    db.commit()
    db.close()


def add_flashcards(flashcard_name, creator_username):

    other_flashcards = get_field('user_info', 'username', creator_username, 'flashcards')
    flashcards = other_flashcards + "%SPLIT%" + flashcard_name

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # get current list of stuff in the row
    command = 'UPDATE user_info SET flashcards = ? WHERE username = ?'
    vars = (flashcards, creator_username)
    c.execute(command, vars)

    db.commit()
    db.close()

    return blog_id


#----------USERINFO-HELPERS----------#


# returns whether or not a user exists
def user_exists(username):
    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    all_users = c.execute("SELECT username FROM user_info")

    for user in all_users:
        if (user[0] == username):
            db.commit()
            db.close()
            return True

    db.commit()
    db.close()
    return False


# checks if provided password in login attempt matches user password
def auth(username, password):
    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    if not user_exists(username):
        db.commit()
        db.close()

        raise ValueError("Username does not exist")

    command = 'SELECT password FROM user_info WHERE username = ?'
    vars = (username,)
    passpointer = c.execute(command, vars)
    real_pass = passpointer.fetchone()[0]

    db.commit()
    db.close()

    password = password.encode('utf-8')

    if real_pass != str(hashlib.sha256(password).hexdigest()):
        raise ValueError("Incorrect password")

    return True



#=============================FLASHCARDS=============================#


#----------FLASHCARDS-ACCESSORS----------#


# get all the flashcard front and backs associated with a certain flashcard
def get_flashcard_content(title):
    fronts = []
    backs = []

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = 'SELECT ? FROM flashcards WHERE title = ? AND card = ?'

    for i in range(len(get_field_list("flashcards", "title", title, "card"))):
        vars = ("front", title, i)
        fronts.append(c.execute(command, vars).fetchone()[0])

        vars = ("back", title, i)
        backs.append(c.execute(command, vars).fetchone()[0])

    db.commit()
    db.close()

    return list(zip(fronts, backs))


# get all flashcards
def get_flashcards():

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    titles = list(set(clean_list(c.execute('SELECT title FROM flashcards').fetchall())))
    data = []

    for i in range(len(titles)):
        data.append((titles[i], get_field("flashcards", "title", titles[i], "creator")))

    db.commit()
    db.close()

    return data


def get_flashcard_creator(title):
    return get_field("flashcards", "title", title, creator)


#----------FLASHCARDS-MUTATORS----------#


def new_flashcard(title, flashcard_content, creator):

    if (flashcard_exists(title)):
        raise ValueError("Title already exists")

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    for i in range(len(flashcard_content)):
        command = 'INSERT INTO flashcards VALUES (?, ?, ?, ?, ?)'
        vars = (title, creator, i, flashcard_content[i][0], flashcard_content[i][1])
        c.execute(command, vars)

    db.commit()
    db.close()

    return title


#----------FLASHCARDS-HELPERS----------#


def flashcard_exists(title):

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    command = 'SELECT * FROM flashcards WHERE title = ?'
    vars = (title,)
    matching_blog = c.execute(command, vars).fetchall()

    if len(matching_blog) > 0:
        db.commit()
        db.close()
        return True

    db.commit()
    db.close()
    return False


#=============================GENERAL=HELPERS=============================#


# used for a bunch of accessor methods; used when only 1 item should be returned
def get_field(table, ID_fieldname, ID, field):
    return get_field_list(table, ID_fieldname, ID, field)[0]


# wrapper method
# used for a bunch of accessor methods; used when a list of items in a certain field should be returned
def get_field_list(table, ID_fieldname, ID, field):

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    command = f'SELECT ? FROM {table} WHERE {ID_fieldname} = ?'
    vars = (field, ID)
    data = c.execute(command, vars).fetchall()

    db.commit()
    db.close()

    return clean_list(data)


# returns a list of every field associated with this id (including the id itself)
def get_all_fields(table, ID_fieldname, ID):

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    command = f'SELECT * FROM {table} WHERE {ID_fieldname} = ?'
    vars = (ID,)
    data = c.execute(command, vars).fetchall()

    db.commit()
    db.close()

    return clean_list(data)


# turn a list of tuples (returned by .fetchall()) into a 1d list
def clean_list(raw_output):

    clean_output = []
    for lst in raw_output:
        for item in lst:
            clean_output.append(item)

    return clean_output


#=============================MAIN=SCRIPT=============================#

# make tables
create_user_info()
create_flashcards()
