import pymysql
from config.config import get_pymysql_connection as get_connection 

def display_public_messages():
    connection = get_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT * FROM public_messages ORDER BY id DESC") # Fetch public messages from the database
    messages = cursor.fetchall()

    cursor.close()
    connection.close()
    return messages

def send_public_message(mentee_id, content, interest):
    connection = get_connection()
    cursor = connection.cursor()

    sql = "INSERT INTO public_messages (sender_id, content, interest) VALUES (%s, %s,%s)"
    cursor.execute(sql, (mentee_id, content, interest))
    connection.commit()

    cursor.close()
    connection.close()

def get_mentee_profile(mentee_id):
    connection = get_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    sql = "SELECT * FROM mentee_profiles WHERE user_id = %s"
    cursor.execute(sql, (mentee_id))
    profile = cursor.fetchone()

    cursor.close()
    connection.close()
    return profile





