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


# blogs
def create_flashcards():

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS blogs (
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


def get_flashcards(username):
    # blog ids are stored as text; split the string (delimiter = space)
    # cut the first item, which is 'None'
    return get_field('user_info', 'username', username, 'flashcards').split(' ')[1:]


#----------USERINFO-MUTATORS----------#


# FUNCTIONAL BUT MORE STUFF TBA
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


# FUNCTIONAL BUT MORE STUFF TBA
def change_username(old_username, new_username):

    if user_exists(new_username):
        raise ValueError("Username already exists")

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # update stuff associated with old username
    command = 'UPDATE blogs SET creator = ? WHERE creator_username = ?'
    vars = (new_username, old_username)
    c.execute(command, vars)

    command = 'UPDATE user_info SET username = ? WHERE username = ?'
    vars = (new_username, old_username)
    c.execute(command, vars)

    db.commit()
    db.close()

    return "success"


# FUNCTIONAL BUT MORE STUFF TBA
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

    command = f'UPDATE user_info SET password = ? WHERE username = ?'
    vars =(new_pass, username)
    c.execute()

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


#----------user_info-HELPERS----------#


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


# FUNCTIONAL BUT MORE STUFF TBA
# checks if provided password in login attempt matches user password
def auth(username, password):
    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    if not user_exists(username):
        db.commit()
        db.close()

        raise ValueError("Username does not exist")

    # hash password here? (MUST MATCH other hash from register)
    command = 'SELECT password FROM user_info WHERE username = ?'
    vars = (username)
    passpointer = c.execute(command, vars)
    real_pass = passpointer.fetchone()[0]

    db.commit()
    db.close()

    password = password.encode('utf-8')

    if real_pass != str(hashlib.sha256(password).hexdigest()):
        raise ValueError("Incorrect password")

    return True



#=============================BLOGS=============================#


#----------BLOG-ACCESSORS----------#


# get all the entry_ids associated with a certain blog
def get_entries(blog_id):
    return get_field_list('entries', 'blog_id', blog_id, 'entry_id')


# get all blogs
def get_blogs():

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    data = c.execute(f'SELECT blog_id FROM blogs').fetchall()

    db.commit()
    db.close()

    return clean_list(data)


def get_blog_name(blog_id):
    return get_field("blogs", "blog_id", blog_id, blog_name)


def get_blog_author(blog_id):
    return get_field("blogs", "blog_id", blog_id, creator_username)


#----------BLOG-MUTATORS----------#


# **YOU SHOULDN'T BE USING THIS** see add_blog in user_info section
# create a *NEW* blog, return ID
def new_blog(blog_name, creator_username):

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    blog_id = gen_id()
    # make sure the id is unique
    while (blog_exists(blog_id)):
        blog_id = gen_id()

    c.execute(f'INSERT INTO blogs VALUES ("{blog_name}", "{blog_id}", "{creator_username}")')

    db.commit()
    db.close()

    return blog_id


# delete blog?


#----------BLOG-HELPERS----------#


# helper for new_blog
def blog_exists(blog_id):

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    matching_blog = c.execute(f'SELECT * FROM blogs WHERE blog_id = "{blog_id}"').fetchall()
    if len(matching_blog) > 0:
        db.commit()
        db.close()
        return True

    db.commit()
    db.close()
    return False


#=============================ENTRIES=============================#


#----------ENTRY-ACCESSORS----------#


def get_entry_name(entry_id):
    return get_field('entries', 'entry_id', entry_id, 'entry_name')


def get_entry_blog(entry_id):
    return get_field('entries', 'entry_id', entry_id, 'blog_id')


def get_entry_udate(entry_id):
    return get_field('entries', 'entry_id', entry_id, 'upload_date')


def get_entry_edate(entry_id):
    return get_field('entries', 'entry_id', entry_id, 'edit_date')


def get_entry_contents(entry_id):
    return get_field('entries', 'entry_id', entry_id, 'contents')


# returns a list of every field associated with this entry_id (besides the id itself)
def get_entry_all(entry_id):
    return get_all_fields('entries', 'entry_id', entry_id)


#----------ENTRY-MUTATORS----------#


# add a *NEW* entry to a blog, return ID
def add_entry(entry_name, blog_id, contents):

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    entry_id = gen_id()
    # make sure the id is unique
    while (entry_exists(entry_id)):
        entry_id = gen_id()

    # retrieve date in yyyy-mm-dd format
    date = datetime.today().strftime('%Y-%m-%d')
    c.execute(f'INSERT INTO entries VALUES ("{entry_name}", "{entry_id}", "{blog_id}", "{date}", "{date}", "{contents}")')

    db.commit()
    db.close()

    return entry_id


# modify the entry_name and/or entry's contents
def update_entry(entry_id, entry_name, contents):

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # get current list of stuff in the row
    c.execute(f'UPDATE entries SET entry_name = "{entry_name}", contents = "{contents}" WHERE entry_id = "{entry_id}"')

    db.commit()
    db.close()


# delete entry?


#----------ENTRY-HELPERS----------#


# helper for add_entry
def entry_exists(entry_id):

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    matching_entry = c.execute(f'SELECT * FROM entries WHERE entry_id = "{entry_id}"').fetchall()
    if len(matching_entry) > 0:
        db.commit()
        db.close()
        return True

    db.commit()
    db.close()
    return False



#=============================GENERAL=HELPERS=============================#


# generate an id
def gen_id():
    # use secrets module to generate a random 32-byte string
    return secrets.token_hex(32)


# used for a bunch of accessor methods; used when only 1 item should be returned
def get_field(table, ID_fieldname, ID, field):
    return get_field_list(table, ID_fieldname, ID, field)[0]


# wrapper method
# used for a bunch of accessor methods; used when a list of items in a certain field should be returned
def get_field_list(table, ID_fieldname, ID, field):

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    data = c.execute(f'SELECT {field} FROM {table} WHERE {ID_fieldname} = "{ID}"').fetchall()

    db.commit()
    db.close()

    return clean_list(data)


# returns a list of every field associated with this id (including the id itself)
def get_all_fields(table, ID_fieldname, ID):

    DB_FILE="data.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    data = c.execute(f'SELECT * FROM {table} WHERE {ID_fieldname} = "{ID}"').fetchall()

    db.commit()
    db.close()

    return clean_list(data)


# turn a list of tuples (returned by .fetchall()) into a 1d list
def clean_list(raw_output):

    clean_output = []
    for lst in raw_output:
        for item in lst:
            clean_output += [item]

    return clean_output


#=============================MAIN=SCRIPT=============================#

# make tables
create_user_data()
create_blog_data()
create_entry_data()
