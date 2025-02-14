from flask import Flask, render_template, request
import webbrowser
import threading

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

# stores data from html form into variables
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

    print(username, password, email, firstName, lastName, Org_School, acc_Type, ID)
    return render_template('accountCreate.html')

# END OF ACCOUNT CREATION CODE


if __name__ == '__main__':
    threading.Timer(1.25, open_browser).start()
    app.run(debug=True)

