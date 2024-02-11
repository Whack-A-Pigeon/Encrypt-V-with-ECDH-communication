# decrypt.py

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import os

# Function to retrieve file details from the database
def fileDetails(comm, client_socket, file_id, username, password):
    
    # Formulate a message to send to server
    message = [file_id.hex(), username, password]

    # Request data from server
    comm.send_message(client_socket, "D " + ','.join(message))

    # Receive data from server
    message = comm.recieve_message(client_socket)
    details = message.split(',')

    # Return the list
    return details

# Function to decrypt bytes using AES-GCM
def decryptBytes(encryptedText, key, iv):
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    try:
        decryptedBytes = unpad(cipher.decrypt(encryptedText), AES.block_size)
        return decryptedBytes
    except (ValueError, KeyError):
        return None
    
# Function to delete encryption records from database   
def deleteRecord(comm, client_socket, file_id, username, password):

    message = [file_id.hex(), username, password]
    print("Deleted Message: ", message)

    # Send message to server, requesting to delete encryption records
    comm.send_message(client_socket, "O " + ','.join(message))

    # Receive confirmation
    message = comm.recieve_message(client_socket)

# Perform decryption
def performDecryption(gui, comm, client_socket, username, password, selectedFile, file_id, encryptedFileBytes):

    try:

        # Get the details of the filename, text used for encryption from database
        details = fileDetails(comm, client_socket, file_id, username, password)

        originalFileName = details[0]
        keyBytes = bytes.fromhex(details[1])
        iv = bytes.fromhex(details[2])

        # With the details, decrypt the file using decryptBytes function
        decryptedBytes = decryptBytes(encryptedFileBytes, keyBytes, iv)

        if decryptedBytes is not None:

            # Get original directory and create a new file with the OG name and dir
            originalDir = os.path.dirname(selectedFile)
            decryptedFile = os.path.join(originalDir, originalFileName)
        
            # Open the file to write and write the contents produced by decryption
            with open(decryptedFile, "wb") as file:
                file.write(decryptedBytes)
            os.remove(selectedFile) # Remove selected file

            # Remove the database record for the particular encryption
            deleteRecord(comm, client_socket, file_id, username, password)

            gui.showMessage("File decrypted successfully and saved as " + os.path.basename(decryptedFile))

        else:
            gui.showMessage("Error decrypting file. Please make sure you selected the correct encryption key.")

    except Exception as e:
        print(e)
        gui.showMessage("Error decrypting file.") 