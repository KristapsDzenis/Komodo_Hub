from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Response
import webbrowser
import threading
import SQL
from datetime import datetime
import base64

app = Flask(__name__)


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

@app.route('/')
def index():
    return render_template('index.html')
# -------------- Account Creation Code -------------- (Kristaps Dzenis)
# renders account creation page
@app.route('/accountCreate.html')
def render_acc_create_page():
    return render_template('accountCreate.html')

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

    print(username, password, email, firstName, lastName, Org_School, acc_Type, ID, image)  # debugger
    SQL.insert_user(username, password, email, firstName, lastName, Org_School, acc_Type, ID, image)    # run sql query
    return render_template('accountCreate.html', success="Congratulations! Account created successfully") # rerender page

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
    print(username, password, email, Org_School, acc_Type, image)               # debugger
    SQL.insert_org(username, password, email, Org_School, acc_Type, image)    # run sql query
    return render_template('accountCreate.html', success="Congratulations! Account created successfully")    # rerender page



# END OF ACCOUNT CREATION CODE

# Main page code (Mykyta Bilous)
   # Everyone can see the feed
    posts = SQL.get_posts()
    for post in posts:
        post['comments'] = SQL.get_comments(post['id'])
    current_user = session.get('username')  # or None if not logged in
    error = request.args.get('error')       # optional error message from login
    return render_template('index.html', posts=posts, current_user=current_user, error=error)

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

SQL.check_db()

def run_app():
    threading.Timer(1.25, open_browser).start()
    app.run(debug=True)

if __name__ == '__main__':
    run_app()
