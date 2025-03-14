# Python file for SQL Queries
import sqlite3

# function to check database and create tables
def check_db():
    connect_db = sqlite3.connect('database.db')    # connect to database
    cursor = connect_db.cursor()                            # define cursor

    # create temperature_sensors table and heating_central tables
    cursor.execute("""CREATE TABLE IF NOT EXISTS user_details(
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    fname TEXT NOT NULL,
    sname TEXT NOT NULL,
    org_school_name TEXT NOT NULL,
    e_mail TEXT NOT NULL,
    account_type TEXT NOT NULL,
    id TEXT,
    profile_image BLOB
    );""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS org_details(
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        org_school_name TEXT NOT NULL,
        e_mail TEXT NOT NULL,
        account_type TEXT NOT NULL,
        profile_image BLOB
        );""")

    connect_db.commit()  # commit changes to database
    connect_db.close()  # close database


# function to insert new user data into user_details table
def insert_user(username, password, email, firstName, lastName, Org_School, acc_Type, ID, image):
    connect_db = sqlite3.connect('database.db')  # connect to database
    cursor = connect_db.cursor()

    cursor.execute("INSERT OR IGNORE INTO user_details VALUES (:username, :password, :fname, :sname, :org_school_name, "
                   ":e_mail, :account_type, :id, :profile_image)", {
        "username": username,
        "password": password,
        "fname": firstName,
        "sname": lastName,
        "org_school_name": Org_School,
        "e_mail": email,
        "account_type": acc_Type,
        "id": ID,
        "profile_image": image
    })

    connect_db.commit()  # commit changes to database
    connect_db.close()  # close database


# function to insert new organisation data into org_details table
def insert_org(username, password, email, Org_School, acc_Type, image) :
    connect_db = sqlite3.connect('database.db')  # connect to database
    cursor = connect_db.cursor()

    cursor.execute("INSERT OR IGNORE INTO org_details VALUES (:username, :password, :org_school_name, "
                   ":e_mail, :account_type, :profile_image)", {
        "username": username,
        "password": password,
        "org_school_name": Org_School,
        "e_mail": email,
        "account_type": acc_Type,
        "profile_image": image
    })

    connect_db.commit()  # commit changes to database
    connect_db.close()  # close database

# function to retrieve user password and account type from user_details table
def fetch_user_details(username, cursor):

    cursor.execute("SELECT password, account_type FROM user_details WHERE username =?", (username,))

    return cursor.fetchall()

# function to retrieve user password and account type from org_details table
def fetch_org_details(username, cursor):

    cursor.execute("SELECT password, account_type FROM org_details WHERE username =?", (username,))

    return cursor.fetchall()

# Add this to check_db() in SQL.py
cursor.execute("""CREATE TABLE IF NOT EXISTS user_posts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    content TEXT,
    image BLOB,
    FOREIGN KEY (username) REFERENCES user_details(username)
);""")

# Insert new post (text + image)
def insert_post(username, content, image):
    connect_db = sqlite3.connect('database.db')
    cursor = connect_db.cursor()

    cursor.execute("INSERT INTO user_posts (username, content, image) VALUES (?, ?, ?)", 
                   (username, content, image))
    
    connect_db.commit()
    connect_db.close()

# Fetch posts (including images)
def fetch_posts(cursor):
    cursor.execute("SELECT username, content, image FROM user_posts ORDER BY id DESC")
    return cursor.fetchall()
