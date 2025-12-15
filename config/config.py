from flask_sqlalchemy import SQLAlchemy
import pymysql 
import os 
import subprocess
import platform  
import bleach 
import time 

def start_mysql_server():
    print("Checking MySQL server status...")
    system_platform = platform.system()
    if system_platform == 'Windows':
        check = subprocess.Popen(['sc', 'query', 'MySQL'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if b'RUNNING' not in check.stdout.read():
            pass
        else:
            check = subprocess.Popen(['net', 'start', 'MySQL'])
            time.sleep(2)  # Wait for a moment to ensure the service starts
            if check.returncode == 0:
                print("MySQL server started successfully.")
    elif system_platform == 'Linux':
        check = subprocess.Popen(['systemctl', 'is-active', 'mysql'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if b'active' not in check.stdout.read():
            pass
        else:
            subprocess.Popen(['sudo', 'service', 'mysql', 'start'])
            time.sleep(2)  # Wait for a moment to ensure the service starts
            if check.returncode == 0:
                print("MySQL server started successfully.")
    elif system_platform == 'Darwin':  # macOS
        check = subprocess.Popen(['brew', 'services', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if b'mysql' not in check.stdout.read():
            pass
        else:
            check = subprocess.Popen(['brew', 'services', 'start', 'mysql'])
            time.sleep(2)  # Wait for a moment to ensure the service starts
            if check.returncode == 0:
                print("MySQL server started successfully.")



def create_database_user(host='localhost'):
    """Create a MySQL user with all privileges on mentor_mentee_db database."""
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password=''  # Change this if your root user has a password
    )
    username = 'mentor_mentee_user'
    password = 'SecurePass123!123'  # Change this!
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT User FROM mysql.user WHERE User = '{username}' AND Host = '{host}'")
    if cursor.fetchone():
        print(f"User '{username}'@'{host}' already exists!")
        cursor.close()
        conn.close()
        return
    # Create user
    cursor.execute(f"CREATE USER '{username}'@'{host}' IDENTIFIED BY '{password}'")
    
    # Grant all privileges on mentor_mentee_db database
    cursor.execute(f"GRANT ALL PRIVILEGES ON mentor_mentee_db.* TO '{username}'@'{host}'")
    
    # Apply changes
    cursor.execute("FLUSH PRIVILEGES")
    
    cursor.close()
    conn.close()
    
    print(f"User '{username}' created successfully!")
    
# SQLAlchemy instance
db = SQLAlchemy()

def create_database_if_not_exists(): # Create database if it doesn't exist
    connection = pymysql.connect(
        host='localhost',
        user='mentor_mentee_user',
        password='SecurePass123!123',
        cursorclass=pymysql.cursors.DictCursor
    )

    with connection.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS mentor_mentee_db")
        print("Database checked/created.")
    connection.commit()
    
# Initialize database
def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mentor_mentee_user:SecurePass123!123@localhost/mentor_mentee_db' #  i have to create database before running this line or i will os module for this, otherise it will through error 
    db.init_app(app)
    return db

# PyMySQL connection for raw queries 
def get_pymysql_connection():
    return pymysql.connect(
        host='localhost',
        user='mentor_mentee_user',
        password='SecurePass123!123',
        db='mentor_mentee_db',
        cursorclass=pymysql.cursors.DictCursor
    )

def create_default_admin(app, db): # Create a default admin user if not exists
    from config.model import User # Importing here to avoid circular imports
    with app.app_context():
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin', password='adminpass', role='admin')
            print("Creating default admin user")
            db.session.add(admin_user)
            db.session.commit()

def add_user(username, password, role, name, interests):
    from config.model import User
    new_user = User(username=username, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()
    if role == 'mentee':
        print("Creating mentee profile")
        from config.model import MenteeProfile
        mentee_profile = MenteeProfile(user_id=new_user.id, name=name, interests=interests)
        db.session.add(mentee_profile)
        db.session.commit()
    elif role == 'mentor':
        print("Creating mentor profile")
        from config.model import MentorProfile, Application
        mentor_profile = MentorProfile(user_id=new_user.id, name=name, field_of_expertise=interests)
        application = Application(user_id=new_user.id, username=username, field_of_expertise=interests, status='pending')
        db.session.add(application)
        db.session.add(mentor_profile)
        db.session.commit()
def approved(mentor_id):
    from config.model import Application
    application = Application.query.filter_by(user_id=mentor_id).first()
    if application and application.status == 'approved':
        return True
    return False

def sanitize_input(user_input):
    # Use bleach to sanitize input
    cleaned_input = bleach.clean(user_input, tags=[],strip=True).strip()
    return cleaned_input