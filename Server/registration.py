# Register.py

from hashpassword import hashPassword

def registerUser(connection, username, password):
    try:
        with connection.cursor() as cursor:
            insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(insert_query, (username, hashPassword(password)))
        connection.commit()
        return True
    except Exception as e:
        print(e)
        return False