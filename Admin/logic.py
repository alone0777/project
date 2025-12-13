import pymysql
from config.config import get_pymysql_connection as get_connection
from config.model import User

# ADMIN LOGIN

def admin_login(username, password):
    admin = User.query.filter_by(username=username, password=password, role='admin').first() # replace with raw query to prevent SQL injection
    return admin


# DASHBOARD COUNTS

def get_dashboard_counts():
    connection = get_connection()
    cursor = connection.cursor()

    data = {}

    # Count total users
    cursor.execute("SELECT COUNT(*) FROM users")
    row = cursor.fetchone()
    data['total_users'] = row['COUNT(*)']   

    # Count mentors
    cursor.execute("SELECT COUNT(*) FROM users WHERE role='mentor'")
    row = cursor.fetchone()
    data['total_mentors'] = row['COUNT(*)']

    # Count mentees
    cursor.execute("SELECT COUNT(*) FROM users WHERE role='mentee'")
    row = cursor.fetchone()
    data['total_mentees'] = row['COUNT(*)']

    # Count pending applications
    cursor.execute("SELECT COUNT(*) FROM applications WHERE status='pending'")
    row = cursor.fetchone()
    data['pending_applications'] = row['COUNT(*)']

    cursor.close()
    connection.close()
    return data



# GET ALL PENDING APPLICATIONS

def get_pending_applications():
    connection = get_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT * FROM applications WHERE status='pending'")
    applications = cursor.fetchall()

    cursor.close()
    connection.close()
    return applications


# APPROVE APPLICATION

def approve_application(app_id):
    connection = get_connection()
    cursor = connection.cursor()

    # Fetch username from application
    cursor.execute("SELECT username FROM applications WHERE id=%s", (app_id,))
    result = cursor.fetchone()

    if result:
        username = result['username']

        # Update application status
        cursor.execute("UPDATE applications SET status='approved' WHERE id=%s", (app_id))

        connection.commit()

    cursor.close()
    connection.close()


# DELETE APPLICATION

def delete_application(app_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM applications WHERE id=%s", (app_id,))
    connection.commit()

    cursor.close()
    connection.close()
