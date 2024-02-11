# storeKey.py

from checkLogin import Authorize

# Store encryption key details to database in files table [Post Encryption process]
def storeKeyInDatabase(decrypted_message, connection):

    # Separate decrypted message
    data = decrypted_message.split(',')

    # Establish data
    username = data[4]
    password = data[5]
    user_id = Authorize(connection, username, password) # Get user ID for the given user
    file_id = bytes.fromhex(data[0])
    FileName = data[1] 
    key_bytes = bytes.fromhex(data[2])
    iv = bytes.fromhex(data[3])

    # Store data into the database
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO files (user_id, file_id, file_name, encryption_key, iv) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (user_id, file_id, FileName, key_bytes, iv))
        connection.commit()
    except Exception as e:
        print(e)