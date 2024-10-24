# src/app.py

from flask import Flask, render_template, request
from register import register_client  # Import the register function

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    return register_client()  # Call the register function from register.py

@app.route('/offline')
def offline():
    return render_template('offline.html')

if __name__ == '__main__':
    app.run(debug=True)
