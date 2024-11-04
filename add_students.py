from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Replace with a more secure key

# MongoDB Connection
connection_string = "mongodb+srv://kumawatr:JhvogRcEEo10IHyI@cluster9.2bjhi.mongodb.net/"
client = MongoClient(connection_string)
db = client['tutoring-platform']  # Database name
students_collection = db['students']  # Collection for students
tutors_collection = db['tutors']  # Collection for tutors
sessions_collection = db['sessions']  # Collection for sessions

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the user already exists
        if students_collection.find_one({'username': username}):
            return "User already exists. Please choose a different username."
        
        # Store user information
        students_collection.insert_one({'username': username, 'password': password})
        return redirect(url_for('login'))  # Redirect to login after registration
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if user credentials are valid
        user = students_collection.find_one({'username': username, 'password': password})
        if user:
            session['student_id'] = str(user['_id'])  # Store student ID in session
            return redirect(url_for('dashboard'))  # Redirect to dashboard after login
        return "Invalid username or password."
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'student_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    # Retrieve tutor data from the database
    tutors = list(tutors_collection.find())
    return render_template('dashboard.html', username=session['student_id'], tutors=tutors)

# Book a Session with Availability Check
@app.route('/book/session', methods=['POST'])
def book_session():
    data = request.json
    student_id = session.get('student_id')
    if not student_id:
        return jsonify({"message": "You need to be logged in to book a session."}), 401

    tutor_id = data['tutor_id']
    session_time = data['session_time']  # Expected in ISO format, e.g., '2023-11-01T15:30:00'

    # Check if the tutor is already booked for this session time
    existing_session = sessions_collection.find_one({
        "tutor_id": tutor_id,
        "session_time": datetime.fromisoformat(session_time)
    })
    if existing_session:
        return jsonify({"message": "The tutor is not available at this time."}), 400

    # Save session details in the sessions collection
    session_data = {
        "student_id": ObjectId(student_id),
        "tutor_id": ObjectId(tutor_id),
        "session_time": datetime.fromisoformat(session_time),
        "booking_date": datetime.now()
    }
    sessions_collection.insert_one(session_data)

    # Update student's session history
    students_collection.update_one(
        {"_id": ObjectId(student_id)},
        {"$push": {"session_history": session_data}}
    )

    return jsonify({"message": "Session booked successfully!"}), 201

if __name__ == '__main__':
    app.run(port=5058, debug=True)
