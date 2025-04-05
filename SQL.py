import sqlite3

def check_db():
    """Create all necessary tables if they don't exist."""
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # user_details table
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

    # posts table with image column
    c.execute("""
        CREATE TABLE IF NOT EXISTS posts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            likes INTEGER DEFAULT 0,
            image BLOB
        );
    """)

    # comments table
    c.execute("""
        CREATE TABLE IF NOT EXISTS comments(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            comment TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY(post_id) REFERENCES posts(id)
        );
    """)

    # post_likes table for toggling likes
    c.execute("""
        CREATE TABLE IF NOT EXISTS post_likes(
            post_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            PRIMARY KEY (post_id, username),
            FOREIGN KEY(post_id) REFERENCES posts(id)
        );
    """)

    conn.commit()
    conn.close()

def insert_user(username, password, email, firstName, lastName, Org_School, acc_Type, ID, image):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""
        INSERT OR IGNORE INTO user_details 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (username, password, firstName, lastName, Org_School, email, acc_Type, ID, image))
    conn.commit()
    conn.close()

def insert_org(username, password, email, Org_School, acc_Type, image):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""
        INSERT OR IGNORE INTO org_details 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (username, password, Org_School, email, acc_Type, image))
    conn.commit()
    conn.close()

def insert_post(username, content, timestamp, image_data=None):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""
        INSERT INTO posts (username, content, timestamp, likes, image)
        VALUES (?, ?, ?, 0, ?)
    """, (username, content, timestamp, image_data))
    conn.commit()
    post_id = c.lastrowid
    conn.close()
    return post_id

# function to retrieve user password and account type from user_details table
def fetch_user_details(username, cursor):

    cursor.execute("SELECT password, account_type FROM user_details WHERE username =?", (username,))

    return cursor.fetchall()

# function to retrieve user password and account type from org_details table
def fetch_org_details(username, cursor):

    cursor.execute("SELECT password, account_type FROM org_details WHERE username =?", (username,))

    return cursor.fetchall()

def get_posts():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""
        SELECT id, username, content, timestamp, likes, image
        FROM posts
        ORDER BY id DESC
    """)
    rows = c.fetchall()
    conn.close()
    posts = []
    for row in rows:
        posts.append({
            "id": row[0],
            "username": row[1],
            "content": row[2],
            "timestamp": row[3],
            "likes": row[4],
            "image": row[5] is not None  # Boolean: True if image exists
        })
    return posts

def get_post_image(post_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT image FROM posts WHERE id=?", (post_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row and row[0] else None

def toggle_like(post_id, username):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Check if the user already liked the post
    c.execute("SELECT COUNT(*) FROM post_likes WHERE post_id=? AND username=?", (post_id, username))
    already_liked = c.fetchone()[0]
    if already_liked == 0:
        # Add the like
        c.execute("INSERT INTO post_likes (post_id, username) VALUES (?, ?)", (post_id, username))
    else:
        # Remove the like
        c.execute("DELETE FROM post_likes WHERE post_id=? AND username=?", (post_id, username))
    # Recalculate total likes
    c.execute("SELECT COUNT(*) FROM post_likes WHERE post_id=?", (post_id,))
    total_likes = c.fetchone()[0]
    c.execute("UPDATE posts SET likes=? WHERE id=?", (total_likes, post_id))
    conn.commit()
    conn.close()
    return total_likes

def insert_comment(post_id, username, comment, timestamp):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""
        INSERT INTO comments (post_id, username, comment, timestamp)
        VALUES (?, ?, ?, ?)
    """, (post_id, username, comment, timestamp))
    conn.commit()
    comment_id = c.lastrowid
    conn.close()
    return comment_id

def get_comments(post_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""
        SELECT id, username, comment, timestamp
        FROM comments
        WHERE post_id=?
        ORDER BY id ASC
    """, (post_id,))
    rows = c.fetchall()
    conn.close()
    comments = []
    for row in rows:
        comments.append({
            "id": row[0],
            "username": row[1],
            "comment": row[2],
            "timestamp": row[3]
        })
    return comments

def check_user_credentials(username, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT password FROM user_details WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    if not row:
        return "username_not_found"
    if row[0] != password:
        return "wrong_password"
    return "ok"

# Insert new post (text + image)
def insert_new_post(username, content, image):
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

if __name__ == '__main__':
    check_db()
