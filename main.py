from flask import Flask, render_template,request, redirect, url_for

from config.config import init_db, create_database_if_not_exists, create_default_admin, add_user  # Initialize database inside config.py
from config.model import User, Application, MentorProfile, MenteeProfile, Message # Import models 
from Admin.routes import admin_bp 
#from mentor import mentor_bp
#from mentee import mentee_bp

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'x9F2kL8sD1qP0yT7wR5bZ3vA6nH4mC2p' # secret key for session management , can include in enviroment for more security

create_database_if_not_exists()  # Create database if it doesn't exist

db = init_db(app) # Initialize database

with app.app_context():
    db.create_all()  # Create tables if they don't exist

create_default_admin(app, db)  # Create default admin user if not exists
  

# Register blueprints with URL prefixes
app.register_blueprint(admin_bp, url_prefix='/admin') # all admin related routes will start with /admin
#app.register_blueprint(mentor_bp, url_prefix='/mentor') # all mentor related routes will start with /mentor
#app.register_blueprint(mentee_bp, url_prefix='/mentee') # all mentee related routes will start with /mentee

# Home route
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/registration')
def registration():
    return render_template('registration.html')
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')  # 'mentee' or 'mentor'
    add_user(username, password, role)
    return redirect(url_for('siginin'))
@app.route('/siginin')
def siginin():
    return render_template('login.html')
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = User.query.filter_by(username=username, password=password).first()
    if user: # if suucessful login redirt to mentte or or mentee dashboard based on role
        # Logic for successful login
        return f"Welcome, {user.username}!"
    else:
        # Logic for failed login
        return "Invalid credentials. Please try again."
if __name__ == '__main__':
    app.run(debug=True)

