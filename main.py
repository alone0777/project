from flask import Flask, render_template

from config.config import init_db  # Initialize database inside config.py
from admin import admin_bp 
from mentor import mentor_bp
from mentee import mentee_bp

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'x9F2kL8sD1qP0yT7wR5bZ3vA6nH4mC2p' # secret key for session management , can include in enviroment for more security

# Initialize database  
db = init_db(app)

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
    return "Registration logic goes here"
if __name__ == '__main__':
    app.run(debug=True)

