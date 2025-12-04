from flask import Flask, render_template,request, redirect, url_for, session, flash

from config.config import init_db, create_database_if_not_exists, create_default_admin, add_user , approved  # Initialize database inside config.py
from config.model import User, Application, MentorProfile, MenteeProfile, PublicMessages # Import models 
from Admin.routes import admin_bp 
from mentor.routes import mentor_bp
from mentee.routes import mentee_bp

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
app.register_blueprint(mentor_bp, url_prefix='/mentor') # all mentor related routes will start with /mentor
app.register_blueprint(mentee_bp, url_prefix='/mentee') # all mentee related routes will start with /mentee

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
    name = request.form.get('name')
    interests = request.form.get('interests')
    add_user(username, password, role, name, interests)
    return redirect(url_for('signin'))
@app.route('/signin')
def signin():
    return render_template('login.html')
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = User.query.filter_by(username=username, password=password).first()
    if user.role == 'mentee':
        session['mentee_id'] = user.id  # Store mentee_id in session
        print ("Mentee logged in with ID:", user.id)
        return redirect(url_for('mentee.public_messages'))
    elif user.role == 'mentor':
        session['mentor_id'] = user.id  # Store mentor_id in session
        mentor_profile = MentorProfile.query.filter_by(user_id=user.id).first()
        session['mentor_expertise']= mentor_profile.field_of_expertise # Store mentor expertise in session
        checked = approved(user.id)
        if checked:
            return redirect(url_for('mentor.messages'))
        return redirect(url_for('mentor.approval_pending'))  
    else:
        return "Invalid credentials. Please try again."
if __name__ == '__main__':
    app.run(debug=True)


