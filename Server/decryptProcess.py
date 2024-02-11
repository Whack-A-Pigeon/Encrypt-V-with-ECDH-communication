# decryptProcess.py

from checkLogin import Authorize

# [Pre Decryption Process]
def getKeyFromDatabase(decrypted_message, connection):

    # Establish data
    data = decrypted_message.split(',')
    file_id = bytes.fromhex(data[0])
    username = data[1]
    password = data[2]
    user_id = Authorize(connection, username, password)
    
    # Retrive details from database
    try:
        with connection.cursor() as cursor:
            query = "SELECT file_name, encryption_key, iv FROM files WHERE file_id = %s AND user_id = %s"
            cursor.execute(query, (file_id, user_id))
            result = cursor.fetchone()
            if result:
                details = [result[0], result[1].hex(), result[2].hex()]
                return details
            
    except Exception as e:
        print(e)
        return None
    
# [Post Decryption Process]
def deleteRecord(decrypted_message, connection):

    # Establish data
    data = decrypted_message.split(',')
    file_id = bytes.fromhex(data[0])
    username = data[1]
    password = data[2]
    user_id = Authorize(connection, username, password)
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM files WHERE file_id = %s AND user_id = %s"
            cursor.execute(query, (file_id, user_id))
        connection.commit()
        return True
    except Exception as e:
        print(e)

