import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from register import register_client  # Import the register function
from login import login_user  # Import the login function

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '../templates'))

# Set the secret key for sessions
app.secret_key = 'your_unique_secret_key_here'

@app.route('/')
def home():
    message = request.args.get('message')  # Get message from URL parameters
    return render_template('index.html', message=message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        result = register_client(request.form)
        if "successfully" in result:
            return redirect(url_for('home', message=result))
        return render_template('register.html', message=result)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return login_user(request.form)  # Call the login function from login.py
    return render_template('login.html')

@app.route('/offline')
def offline():
    return render_template('offline.html')

if __name__ == '__main__':
    app.run(debug=True)
