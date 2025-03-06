# Python Flask file
from flask import Flask, render_template, request
import webbrowser
import threading
import SQL
import base64

app = Flask(__name__)

# opens web browser with specified address with flask app
def open_browser():
    """Open the default web browser when the server starts."""
    webbrowser.open_new("http://127.0.0.1:5000/")

# renders index page, '/' means first page rendered with flask
@app.route('/')
def index():
    return render_template('index.html')

# ACCOUNT CREATION CODE (Kristaps Dzenis)

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

    print(username, password, email, firstName, lastName, Org_School, acc_Type, ID, image)  # debugger
    SQL.insert_user(username, password, email, firstName, lastName, Org_School, acc_Type, ID, image)    # run sql query
    return render_template('accountCreate.html', success="Congratulations! Account created successfully") # rerender page

# stores data from html form into SQLite database
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

    print(username, password, email, Org_School, acc_Type, image)  # debugger
    SQL.insert_org(username, password, email, Org_School, acc_Type, image)    # run sql query
    return render_template('accountCreate.html', success="Congratulations! Account created successfully")    # rerender page

# END OF ACCOUNT CREATION CODE

# ADMIN PANEL CODE (Milo Byrnes)

# renders admin panel page with dummy data
@app.route('/admin.html')
def render_admin_panel():
    dummy_data = [
        {'id': 1, 'username': 'alice', 'email': 'alice@example.com'},
        {'id': 2, 'username': 'bob', 'email': 'bob@example.com'},
        {'id': 3, 'username': 'charlie', 'email': 'charlie@example.com'},
        {'id': 4, 'username': 'david', 'email': 'david@example.com'},
        {'id': 5, 'username': 'eve', 'email': 'eve@example.com'}
    ]
    return render_template('admin.html', dummy_data=dummy_data)

# END OF ADMIN PANEL CODE

SQL.check_db()
if __name__ == '__main__':
    threading.Timer(1.25, open_browser).start()
    app.run(debug=True)
