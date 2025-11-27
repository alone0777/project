from flask_sqlalchemy import SQLAlchemy
import pymysql 
import os 

def start_mysql_server():
    # Function to start MySQL server if needed
    pass    
    
# SQLAlchemy instance
db = SQLAlchemy()

def create_database_if_not_exists(): # Create database if it doesn't exist
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        cursorclass=pymysql.cursors.DictCursor
    )

    with connection.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS mentor_mentee_db")
        print("Database checked/created.")
    connection.commit()
    
# Initialize database
def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/mentor_mentee_db' #  i have to create database before running this line or i will os module for this, otherise it will through error 
    db.init_app(app)
    return db

# PyMySQL connection for raw queries 
def get_pymysql_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
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

def add_user(username, password, role):
    from config.model import User
    new_user = User(username=username, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()
    if role == 'mentor':
        print("Creating mentor profile")
        from config.model import MentorProfile, Application
        mentor_profile = MentorProfile(user_id=new_user.id)
        application = Application(user_id=new_user.id, username=username)
        db.session.add(application)
        db.session.add(mentor_profile)
        db.session.commit()