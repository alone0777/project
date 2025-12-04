from config.config import db

#  Users table 
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)  # Auto-increment primary key it will be used to identify each user uniquely
    username = db.Column(db.String(100), nullable=False, unique=True) #  to have unique username 
    password = db.Column(db.String(255), nullable=False)  # plain text 
    role = db.Column(db.Enum('mentee', 'mentor', 'admin'), nullable=False)

# Mentor Applications approval table 
class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)  # Auto-increment
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) #foreign key to users table
    username = db.Column(db.String(100), nullable=False)  # applicant username
    field_of_expertise = db.Column(db.String(255), nullable=True) #nullabe used here these filed can have empty value
    status = db.Column(db.Enum('pending','approved','rejected'), default='pending')


# --- Mentor Profile ---
class MentorProfile(db.Model):
    __tablename__ = 'mentor_profiles'
    
    id = db.Column(db.Integer, primary_key=True)  # Auto-increment
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    field_of_expertise = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255), nullable=True)


# --- Mentee Profile ---
class MenteeProfile(db.Model):
    __tablename__ = 'mentee_profiles'
    
    id = db.Column(db.Integer, primary_key=True)  # Auto-increment
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    interests = db.Column(db.Text, nullable=True)
    name = db.Column(db.String(255), nullable=True)


# --- Messages ---
class PublicMessages(db.Model):
    __tablename__ = 'public_messages'
    
    id = db.Column(db.Integer, primary_key=True)  # Auto-increment
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    interest = db.Column(db.String(255), nullable=True) 

