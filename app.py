from flask import Flask, render_template, request, redirect, url_for, abort
import json, os, uuid

app = Flask(__name__)

DATA_FILE = 'data.json'
ADMIN_PASSWORD = 'kashikabajpai'  # Change this!

# Load & Save Data
def load_data():
    if not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0:
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Routes
@app.route('/')
def index():
    return render_template('add_user.html')

@app.route('/add', methods=['POST'])
def add_user():
    # Password check
    admin_pass = request.form['password']
    if admin_pass != ADMIN_PASSWORD:
        return "Unauthorized: Incorrect admin password", 401

    # Extract form data
    name = request.form['name']
    event = request.form['event']
    application_no = request.form['application_no']
    submit_date = request.form['submit_date']
    event_date = request.form['event_date']
    status = request.form['status']

    # Load and check uniqueness of application_no
    data = load_data()
    for user in data.values():
        if user['application_no'] == application_no:
            return "Application No. already exists!", 400

    # Generate unique user ID (UUID)
    user_id = str(uuid.uuid4())[:8]  # Short UUID

    # Save data
    data[user_id] = {
        'name': name,
        'event': event,
        'application_no': application_no,
        'submit_date': submit_date,
        'event_date': event_date,
        'status': status
    }
    save_data(data)

    return redirect(url_for('show_user', user_id=user_id))

@app.route('/user/<user_id>')
def show_user(user_id):
    data = load_data()
    user = data.get(user_id)
    if not user:
        return "User not found", 404
    return render_template('user.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
