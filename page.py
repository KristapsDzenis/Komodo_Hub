
# Python Flask file
from flask import Flask, render_template, request, redirect, url_for, jsonify, Response, session
import webbrowser
import threading
import SQL
import sqlite3
from datetime import datetime
import base64

app = Flask(__name__)
app.secret_key = "123456789"


# opens web browser with specified address with flask app

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

# renders index page, '/' means first page rendered with flask
@app.route('/')
def index():
    posts = SQL.get_posts()
    for post in posts:
        post['comments'] = SQL.get_comments(post['id'])
    current_user = session.get('username')
    account_type = session.get('account_type')
    error = request.args.get('error')
    return render_template('index.html', posts=posts, current_user=current_user, account_type=account_type, error=error)



# ACCOUNT CREATION AND LOGIN CODE (Kristaps Dzenis)

# function to process user login details and direct to correct page
"""@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('Username')
    password = request.form.get('Password')
    # For simplicity, we ignore "source_page" now.
    if SQL.check_user_credentials(username, password) == "ok":
        session['username'] = username  # Set the logged-in user in session
        return redirect(url_for('index'))
    else:
        return render_template('index.html', error="Invalid username or password")"""

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('Username')
    password = request.form.get('Password')
    source_page = request.form.get('source_page')
    print(username, password, source_page)          # debugger

    # retrieve user password and account type from db based on username
    connect_db = sqlite3.connect('database.db')  # connect to database
    cursor = connect_db.cursor()
    data = SQL.fetch_user_details(username, cursor)     # check user_details for details
    if not data:
        data = SQL.fetch_org_details(username, cursor)      # check org_details for details
        if not data:
            #if username not found throw error
            if source_page == "index.html":
                return render_template('index.html', error="Invalid username or password")
            if source_page == "accountCreate.html":
                return render_template('accountCreate.html', error="Invalid username or password")
    print(data)         # debugger
    connect_db.close()  # close database

    # check password and if password correct direct to correct page based on account type
    if SQL.check_user_credentials(username, password) == "ok":
        session['username'] = username  # Set the logged-in user in session
        session['account_type'] = data[0][1]
        return redirect(url_for('index'))
    # if password incorrect throw error
    else:
        if source_page == "index.html":
            return render_template('index.html', error="Invalid username or password")
        if source_page == "accountCreate.html":
            return render_template('accountCreate.html', error="Invalid username or password")




@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# renders account creation page
@app.route('/accountCreate.html')
def render_acc_create_page():
    return render_template('accountCreate.html')

# stores data from html form into SQLite database
@app.route('/create_account', methods=['POST'])
def create_account():
    username = request.form.get('Username')
    password = request.form.get('Password')
    email = request.form.get('Email')
    firstName = request.form.get('First Name')
    lastName = request.form.get('Last Name')
    Org_School = request.form.get('OrgName')
    acc_Type = request.form.get('Type')
    ID = request.form.get('ID Number')
    # stores image in variable and converts to binary
    image = request.files['image']
    image = image.read()

    connect_db = sqlite3.connect('database.db')  # connect to database
    cursor = connect_db.cursor()
    data = SQL.fetch_user_details(username, cursor)
    connect_db.close()  # close database

    if not data:
        print(username, password, email, firstName, lastName, Org_School, acc_Type, ID, image)  # debugger
        SQL.insert_user(username, password, email, firstName, lastName, Org_School, acc_Type, ID, image)    # run sql query
        return render_template('accountCreate.html', success="Congratulations! Account created successfully") # rerender page
    else:
        return render_template('accountCreate.html', error2="Username already exists!\nTry different username")  # rerender page

@app.route('/create_org', methods=['POST'])
def create_org():
    username = request.form.get('Username')
    password = request.form.get('Password')
    email = request.form.get('Email')
    Org_School = request.form.get('OrgName')
    acc_Type = "Admin"
   # stores image in variable and converts to binary
    image = request.files['image']
    image = image.read()

    connect_db = sqlite3.connect('database.db')  # connect to database
    cursor = connect_db.cursor()
    data = SQL.fetch_org_details(username, cursor)
    connect_db.close()  # close database

    if not data:
        print(username, password, email, Org_School, acc_Type, image)  # debugger
        SQL.insert_org(username, password, email, Org_School, acc_Type, image)    # run sql query
        return render_template('accountCreate.html', success="Congratulations! Account created successfully")    # rerender page
    else:
        return render_template('accountCreate.html', error2="Username already exists!\nTry different username")  # rerender page



# END OF ACCOUNT CREATION CODE

# Main page code (Mykyta Bilous)
   # Everyone can see the feed\

def index():
    connect_db = sqlite3.connect('database.db')
    cursor = connect_db.cursor()

    # Fetch posts from the database
    posts = SQL.fetch_posts(cursor)
    processed_posts = []
    for post in posts:
        encoded_image = None
        if post[2]:
            encoded_image = base64.b64encode(post[2]).decode('utf-8')
        processed_posts.append({
            'author': post[0],
            'content': post[1],
            'image': encoded_image,
            'likes': post[3],
            'hasImage': bool(post[2])
        })

    connect_db.close()
    return render_template('index.html', posts=processed_posts)#

@app.route('/post_image/<int:post_id>')
def post_image(post_id):
    image_data = SQL.get_post_image(post_id)
    if not image_data:
        return "", 404
    return Response(image_data, mimetype='image/jpeg')

# -------------- New Post, Like, Comment --------------
@app.route('/new_post', methods=['POST'])
def new_post():
    if 'username' not in session:
        return jsonify({"success": False, "error": "Not logged in"}), 403
    username = session['username']
    content = request.form.get('content')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    image_file = request.files.get('image')
    image_data = image_file.read() if image_file else None

    post_id = SQL.insert_post(username, content, timestamp, image_data)
    return jsonify({
        "success": True,
        "post": {
            "id": post_id,
            "username": username,
            "content": content,
            "timestamp": "Just now",
            "likes": 0,
            "hasImage": bool(image_data)
        }
    })
        


@app.route('/like_post', methods=['POST'])
def like_post():
    if 'username' not in session:
        return jsonify({"success": False, "error": "Not logged in"}), 403
    data = request.get_json()
    post_id = data.get("post_id")
    username = session['username']
    new_likes = SQL.toggle_like(post_id, username)
    return jsonify({"success": True, "new_likes": new_likes})

@app.route('/add_comment', methods=['POST'])
def add_comment():
    if 'username' not in session:
        return jsonify({"success": False, "error": "Not logged in"}), 403
    data = request.get_json()
    post_id = data.get("post_id")
    username = session['username']
    comment = data.get("comment")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    comment_id = SQL.insert_comment(post_id, username, comment, timestamp)
    return jsonify({
        "success": True,
        "comment": {
            "id": comment_id,
            "username": username,
            "comment": comment,
            "timestamp": timestamp
        }
    })
# ADMIN PANEL CODE (Milo Byrnes)

# changed by including username variable passed from login function
# renders admin panel page with dummy data
@app.route('/admin/<username>')
def render_admin_panel(username):
    # Get the active section from query parameter, default to 'users-section'
    active_section = request.args.get('section', 'users-section')
    
    connect_db = sqlite3.connect('database.db')
    cursor = connect_db.cursor()
    
    # Fetch regular users with all details
    cursor.execute("""
        SELECT username, password, e_mail, fname, sname, org_school_name, account_type, id 
        FROM user_details
        WHERE account_type != 'Admin'
        ORDER BY username
    """)
    
    users = [
        {
            'username': row[0],
            'password': row[1],
            'email': row[2],
            'fname': row[3],
            'sname': row[4],
            'organization': row[5],
            'account_type': row[6],
            'id': row[7]
        }
        for row in cursor.fetchall()
    ]
    
    # Fetch all organizations
    cursor.execute("""
        SELECT username, password, org_school_name, e_mail, account_type 
        FROM org_details
        ORDER BY username
    """)
    
    organizations = [
        {
            'username': row[0],
            'password': row[1],
            'org_school_name': row[2],
            'email': row[3],
            'account_type': row[4]
        }
        for row in cursor.fetchall()
    ]
    
    connect_db.close()
    return render_template('admin.html', 
                         users=users, 
                         organizations=organizations, 
                         admin_username=username,
                         active_section=active_section)


@app.route('/admin/delete_user/<username>', methods=['POST'])
def delete_user(username):
    try:
        connect_db = sqlite3.connect('database.db')
        cursor = connect_db.cursor()
        
        # Delete the user from the database
        cursor.execute("DELETE FROM user_details WHERE username = ?", (username,))
        connect_db.commit()
        connect_db.close()
        
        # Get the admin username from the referrer URL
        admin_username = request.referrer.split('/admin/')[1].split('?')[0]
        # Get the current section from the referrer
        current_url = request.referrer
        section = 'users-section'  # default
        if '?section=' in current_url:
            section = current_url.split('?section=')[1]
        
        return redirect(url_for('render_admin_panel', username=admin_username, section=section))
    except Exception as e:
        return f"Error deleting user: {str(e)}", 500

@app.route('/admin/delete_organization/<username>', methods=['POST'])
def delete_organization(username):
    try:
        connect_db = sqlite3.connect('database.db')
        cursor = connect_db.cursor()
        
        # Delete the organization from the database
        cursor.execute("DELETE FROM org_details WHERE username = ?", (username,))
        connect_db.commit()
        connect_db.close()
        
        # Get the admin username from the referrer URL
        admin_username = request.referrer.split('/admin/')[1].split('?')[0]
        # Get the current section from the referrer
        current_url = request.referrer
        section = 'organizations-section'  # default to organizations for org deletion
        if '?section=' in current_url:
            section = current_url.split('?section=')[1]
        
        return redirect(url_for('render_admin_panel', username=admin_username, section=section))
    except Exception as e:
        return f"Error deleting organization: {str(e)}", 500

@app.route('/admin/edit_user/<username>', methods=['POST'])
def edit_user(username):
    try:
        data = request.get_json()
        connect_db = sqlite3.connect('database.db')
        cursor = connect_db.cursor()
        
        # Update user details
        cursor.execute("""
            UPDATE user_details 
            SET e_mail = ?, fname = ?, sname = ?, org_school_name = ?, 
                account_type = ?, id = ?
            WHERE username = ?
        """, (
            data['email'], data['fname'], data['sname'], 
            data['organization'], data['account_type'], 
            data['id'], username
        ))
        
        connect_db.commit()
        connect_db.close()
        
        return jsonify({'success': True, 'message': f'User {username} updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/admin/edit_organization/<username>', methods=['POST'])
def edit_organization(username):
    try:
        data = request.get_json()
        connect_db = sqlite3.connect('database.db')
        cursor = connect_db.cursor()
        
        # Update organization details
        cursor.execute("""
            UPDATE org_details 
            SET e_mail = ?, org_school_name = ?, account_type = ?
            WHERE username = ?
        """, (
            data['email'], data['org_school_name'], 
            data['account_type'], username
        ))
        
        connect_db.commit()
        connect_db.close()
        
        return jsonify({'success': True, 'message': f'Organization {username} updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# END OF ADMIN PANEL CODE

# ACCOUNT DETAILS CODE (Prince Kalu)

@app.route('/account/<username>')
def account(username):
    connect_db = sqlite3.connect('database.db')
    cursor = connect_db.cursor()

    # Fetch user info
    cursor.execute("SELECT fname, sname, e_mail, account_type FROM user_details WHERE username = ?", (username,))
    user = cursor.fetchone()

    # Fetch posts
    posts = SQL.fetch_posts(cursor)
    processed_posts = []
    for post in posts:
        encoded_image = None
        if post[2]:
            encoded_image = base64.b64encode(post[2]).decode('utf-8')
        processed_posts.append({
            'author': post[0],
            'content': post[1],
            'image': encoded_image
        })

    connect_db.close()

    if user:
        user_data = {
            'name': f"{user[0]} {user[1]}",
            'email': user[2],
            'role': user[3]
        }
        return render_template('account.html', username=username, user=user_data, posts=processed_posts)
    else:
        return redirect(url_for('index'))

# END OF ACCOUNT DETAILS CODE


# USER MAIN CODE (Stefan Barbu)

# Function to establish a connection to the SQLite database ===
def get_db_connection():
    conn = sqlite3.connect('database.db')  # Connects to the database file
    conn.row_factory = sqlite3.Row         # Enables row data to be accessed like dictionaries
    return conn

# Route to render a user's organisation or personal profile page ===
@app.route('/renderpage/<admin_username>')
def renderpage(admin_username):
    # Connect to the database
    connect_db = sqlite3.connect('database.db')
    cursor = connect_db.cursor()

    # Try to fetch data assuming the user is an organisation admin
    data = SQL.fetch_org_details(admin_username, cursor)

    # If no organisation data found, try fetching user account details instead
    if not data:
       data = SQL.fetch_user_details(admin_username, cursor)

    # Close the database connection once data is retrieved
    connect_db.close()

    # Render the appropriate user page, passing through:
    return render_template('userMain.html',
                           username=admin_username,
                           var1 = data[0][1], # - var1 = user type (Teacher or student)
                           var2 = data[0][2]) # var 2 = user type organization


# END OF USER MAIN CODE


SQL.check_db()

def run_app():
    threading.Timer(1.25, open_browser).start()
    app.run(debug=True)

if __name__ == '__main__':
    run_app()