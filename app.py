from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os, uuid

app = Flask(__name__)

# Configuration for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///users.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ADMIN_PASSWORD = 'kashikabajpai'  # Change this to a secure password

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    event = db.Column(db.String(100))
    application_no = db.Column(db.String(50), unique=True, nullable=False)
    submit_date = db.Column(db.String(50))
    event_date = db.Column(db.String(50))
    status = db.Column(db.String(50))
    unique_id = db.Column(db.String(100), unique=True)

# Ensure database tables are created safely
with app.app_context():
    db.create_all()

# Home route to render add user form
@app.route('/')
def index():
    return render_template('add_user.html')

# Add user route
@app.route('/add', methods=['POST'])
def add_user():
    # Password check
    admin_pass = request.form.get('password')
    if admin_pass != ADMIN_PASSWORD:
        return "Unauthorized: Incorrect admin password", 401

    # Extract form data
    name = request.form.get('name')
    event = request.form.get('event')
    application_no = request.form.get('application_no')
    submit_date = request.form.get('submit_date')
    event_date = request.form.get('event_date')
    status = request.form.get('status')

    # Check for existing application number
    if User.query.filter_by(application_no=application_no).first():
        return "Application No. already exists!", 400

    # Generate unique user ID
    unique_id = str(uuid.uuid4())[:8]

    # Create new user
    new_user = User(
        name=name,
        event=event,
        application_no=application_no,
        submit_date=submit_date,
        event_date=event_date,
        status=status,
        unique_id=unique_id
    )

    # Add and commit to database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('show_user', user_id=unique_id))

# Display user details
@app.route('/user/<user_id>')
def show_user(user_id):
    user = User.query.filter_by(unique_id=user_id).first()
    if not user:
        return "User not found", 404
    return render_template('user.html', user=user)

# Run app
if __name__ == '__main__':
    app.run(debug=True)
