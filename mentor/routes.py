from flask import Blueprint, render_template, request, redirect, url_for, session, flash    
from mentor.logic import ( send_public_message, get_public_messages, get_mentor_profile)
from config.config import sanitize_input    
mentor_bp = Blueprint(
    'mentor',
    __name__,
    template_folder='templates',
    static_folder='static'
)   
 
# MENTor get all  public questions and messages route
@mentor_bp.route('/messages')
def messages():
    if not session.get('mentor_login'): # Check if mentor is logged in
        return redirect(url_for('access_denied'))
    result = get_public_messages()
    expertises=session.get('mentor_expertise').split(',') if session.get('mentor_expertise') else []
    return render_template('messages.html', messages=result, expertises=expertises) 

@mentor_bp.route('/public_messages',methods=['GET'])
def public_messages():
    if not session.get('mentor_login'): # Check if mentor is logged in
        return redirect(url_for('access_denied'))
    is_redirect = request.args.get('from_redirect') == '1'
    if is_redirect:
        expertise = session.get('mentor_expertise_chosen')
        result = get_public_messages(expertise)
        expertises=session.get('mentor_expertise').split(',') if session.get('mentor_expertise') else []
        return render_template('public_messages.html', messages=result, expertises=expertises)
    expertise = request.args.get('expertise')
    session['mentor_expertise_chosen']=expertise
    result = get_public_messages(expertise)
    expertises=session.get('mentor_expertise').split(',') if session.get('mentor_expertise') else []
    return render_template('public_messages.html', messages=result, expertises=expertises)


@mentor_bp.route('/send_message', methods=['POST'])
def send_message():
    if not session.get('mentor_login'): # Check if mentor is logged in
        return redirect(url_for('access_denied'))
    if request.method == 'POST':
        mentor_id = session.get('mentor_id')  # Assuming mentee_id is stored in session
        content = sanitize_input(request.form.get('content')) #  input sanitation
        expertise=session.get('mentor_expertise_chosen')
        send_public_message(mentor_id, content,expertise)
    return redirect(url_for('mentor.messages',from_redirect=1))
    

# MENTEE profile route
@mentor_bp.route('/profile')
def profile():
    if not session.get('mentor_login'): # Check if mentor is logged in
        return redirect(url_for('access_denied'))
    profile = get_mentor_profile(session.get('mentor_id'))
    return render_template('profile.html', profile=profile)

@mentor_bp.route('/approval_pending')
def approval_pending():
    return render_template('approval_pending.html') 

@mentor_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signin'))    