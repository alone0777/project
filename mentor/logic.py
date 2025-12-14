import pymysql
from config.config import get_pymysql_connection as get_connection , db
from config.model import PublicMessages

def display_public_messages():
    connection = get_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT public_messages.* , users.username from public_messages JOIN users ON public_messages.sender_id = users.id ORDER BY id DESC") # Fetch public messages from the database
    messages = cursor.fetchall()

    cursor.close()
    connection.close()
    return messages

def send_public_message(mentor_id, content,expertise):
    new_message = PublicMessages(sender_id=mentor_id, content=content, interest=expertise) # implemneted using sqlchemy to prevent SQL injection
    db.session.add(new_message)
    db.session.commit()

def get_mentor_profile(mentor_id):
    connection = get_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    sql = "SELECT name, field_of_expertise FROM mentor_profiles WHERE user_id = %s"
    cursor.execute(sql, (mentor_id))
    profile = cursor.fetchone()

    cursor.close()
    connection.close()
    return profile

def get_public_messages(expertise=None):
    connection = get_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    if expertise:
        sql = "SELECT public_messages.* , users.username from public_messages JOIN users ON public_messages.sender_id = users.id WHERE interest = %s ORDER BY id DESC"
        cursor.execute(sql, (expertise))
    else:
        sql = "SELECT public_messages.* , users.username from public_messages JOIN users ON public_messages.sender_id = users.id ORDER BY id DESC"
        cursor.execute(sql)     
    messages = cursor.fetchall()
    cursor.close()
    connection.close()
    return messages     





