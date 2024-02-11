from hashpassword import hashPassword

# Authorize user
def Authorize(connection, username, password):
    try:
        with connection.cursor() as cursor:
            # Query to get userId from USERS table for the given username and password
            query = "SELECT user_id FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, hashPassword(password)))
            result = cursor.fetchone()
            if result:
                return result[0]
    except Exception as e:
        print(e)
    return -1