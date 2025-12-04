from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from mentee.logic import ( send_public_message, display_public_messages, get_mentee_profile)    
mentee_bp = Blueprint(
    'mentee',
    __name__,
    template_folder='templates',
    static_folder='static'
)   
 
# MENTEE  public questions and messages route
@mentee_bp.route('/public_messages')
def public_messages():
    result = display_public_messages()
    return render_template('message.html', messages=result) 

@mentee_bp.route('/send_message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        print("Sending message")
        mentee_id = session.get('mentee_id')  # Assuming mentee_id is stored in session
        print("Mentee ID:", mentee_id)
        content = request.form.get('message')
        interest = request.form.get('Interest')
        send_public_message(mentee_id, content,interest)
    return redirect(url_for('mentee.public_messages'))
    

# MENTEE profile route
@mentee_bp.route('/profile')
def profile():
    result = get_mentee_profile(session.get('mentee_id'))
    return render_template('profile.html', profile=result)

@mentee_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signin'))







