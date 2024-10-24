# src/app.py

import os
from flask import Flask, render_template, request, redirect, url_for
from register import register_client  # Import the register function

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '../templates'))

# Set the secret key for sessions
app.secret_key = 'your_unique_secret_key_here'

@app.route('/')
def home():
    message = request.args.get('message')  # Get message from URL parameters
    return render_template('index.html', message=message)

@app.route('/register', methods=['GET', 'POST'])  # Allow both GET and POST
def register():
    if request.method == 'POST':
        result = register_client(request.form)  # Call the register function
        if "successfully" in result:  # Check if the result is a success message
            return redirect(url_for('home', message=result))  # Redirect to home with success message
        return render_template('register.html', message=result)  # Render the registration page with error message
    return render_template('register.html')  # Serve the registration form for GET requests

@app.route('/offline')
def offline():
    return render_template('offline.html')

if __name__ == '__main__':
    app.run(debug=True)
