from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from Admin.logic import (
    admin_login,
    get_dashboard_counts,
    get_pending_applications,
    approve_application,
    delete_application
)

admin_bp = Blueprint(
    'admin',
    __name__,
    template_folder='templates',
    static_folder='static'
)

# ADMIN LOGIN PAGE routes 
@admin_bp.route('/')
def signin():
    return render_template('admin_login.html')

@admin_bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        admin = admin_login(username, password)

        if admin:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password', 'error') # chnage message type to 'error'

    return render_template('admin_login.html')



# ADMIN DASHBOARD
@admin_bp.route('/dashboard')
def dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.signin'))

    counts = get_dashboard_counts()
    return render_template('admin_dashboard.html', counts=counts)



# VIEW PENDING APPLICATIONS

@admin_bp.route('/applications')
def view_applications():
    #if not session.get('admin_logged_in'):
        #return redirect(url_for('admin.login'))

    apps = get_pending_applications()
    return render_template('admin_applications.html', applications=apps)


# APPROVE APPLICATION

@admin_bp.route('/approve/<int:app_id>')
def approve(app_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))

    approve_application(app_id)
    flash('Application approved successfully!', 'success')
    return redirect(url_for('admin.view_applications'))



# DELETE APPLICATION
@admin_bp.route('/delete/<int:app_id>')
def delete(app_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))

    delete_application(app_id)
    flash('Application deleted successfully!', 'success')
    return redirect(url_for('admin.view_applications'))


# LOGOUT
@admin_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signin'))
