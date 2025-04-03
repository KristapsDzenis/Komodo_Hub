import sqlite3

def check_db():
    """Create all necessary tables if they don't exist."""
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # create temperature_sensors table and heating_central tables
    c.execute("""CREATE TABLE IF NOT EXISTS user_details(
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

    # org_details table
    c.execute("""CREATE TABLE IF NOT EXISTS org_details(
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
