from flask_sqlalchemy import SQLAlchemy
import pymysql

# SQLAlchemy instance
db = SQLAlchemy()

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
