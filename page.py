# Python Flask file
from flask import Flask, render_template, request, redirect, url_for
import webbrowser
import threading
import SQL
import sqlite3
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

# ACCOUNT CREATION AND LOGIN CODE (Kristaps Dzenis)

# function to process user login details and direct to correct page
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
            # if username not found throw error
            if source_page == "index.html":
                return render_template('index.html', error="Invalid username or password")
            if source_page == "accountCreate.html":
                return render_template('accountCreate.html', error="Invalid username or password")
    print(data)         # debugger
    connect_db.close()  # close database

    # check password and if password correct direct to correct page based on account type
    if password == data[0][0]:
        if data[0][1] in ["Standard", "Teacher", "Student"]:
            return redirect(url_for('account', username=username))
        if data[0][1] == "Admin":
            return redirect(url_for('render_admin_panel', username=username))
    # if password incorrect throw error
    else:
        if source_page == "index.html":
            return render_template('index.html', error="Invalid username or password")
        if source_page == "accountCreate.html":
            return render_template('accountCreate.html', error="Invalid username or password")

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
    SQL.insert_user(username, password, email, firstName, lastNa
