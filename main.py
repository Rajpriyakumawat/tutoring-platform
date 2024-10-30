from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Simulated user database
users = []

@app.route('/')
def home():
    return render_template('index.html')  # Your home page

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the user already exists
        for user in users:
            if user['username'] == username:
                return "User already exists. Please choose a different username."
        
        # Store user information
        users.append({'username': username, 'password': password})
        return redirect(url_for('login'))  # Redirect to login after registration
    return render_template('register.html')  # Your registration page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if user credentials are valid
        for user in users:
            if user['username'] == username and user['password'] == password:
                session['username'] = username
                return redirect(url_for('dashboard'))  # Redirect to dashboard after login
        return "Invalid username or password."
    return render_template('login.html')  # Your login page

@app.route('/dashboard')
def dashboard():
    return f"Welcome, {session.get('username')}!"

if __name__ == '__main__':
    app.run(port=5050)  # Listen on port 5050
