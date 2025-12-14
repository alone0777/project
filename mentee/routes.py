from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from mentee.logic import ( send_public_message, display_public_messages, get_mentee_profile)
from config.config import sanitize_input    
mentee_bp = Blueprint(
    'mentee',
    __name__,
    template_folder='templates',
    static_folder='static'
)   
 
# MENTEE  public questions and messages route
@mentee_bp.route('/public_messages')
def public_messages():
    if not session.get('mentee_login'): # Check if mentee is logged in
        return redirect(url_for('access_denied'))
    result = display_public_messages()
    return render_template('message.html', messages=result) 

@mentee_bp.route('/send_message', methods=['POST'])
def send_message():
    if not session.get('mentee_login'): # Check if mentee is logged in
        return redirect(url_for('access_denied'))
    if request.method == 'POST':
        print("Sending message")
        mentee_id = session.get('mentee_id')  # Assuming mentee_id is stored in session
        print("Mentee ID:", mentee_id)
        content = sanitize_input(request.form.get('message')) # Sanitize input
        interest = sanitize_input(request.form.get('Interest')) # Sanitize input
        send_public_message(mentee_id, content,interest)
    return redirect(url_for('mentee.public_messages'))
    

# MENTEE profile route
@mentee_bp.route('/profile')
def profile():
    if not session.get('mentee_login'): # Check if mentee is logged in
        return redirect(url_for('access_denied'))
    result = get_mentee_profile(session.get('mentee_id'))
    print(result)
    return render_template('profille.html', profile=result)

@mentee_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signin'))







