# encrypt.py
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import os
import random
import string

# Function to generate a random encryption key
def generateRandomKey():
    return get_random_bytes(32)

# Function to generate a random file name
def generateRandomFileName():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

# Function to encrypt bytes using AES-GCM
def encryptBytes(bytes, key):
    cipher = AES.new(key, AES.MODE_GCM)
    encryptedBytes, tag = cipher.encrypt_and_digest(pad(bytes, AES.block_size))
    return encryptedBytes, cipher.nonce

# Function to send metadata to server
def sendkeys(comm, client_socket, fileId, originalFileName, keyBytes, iv, username, password):
    # Form message
    encrypt_data_list = [fileId, originalFileName, keyBytes, iv, username, password]

    # Send details to the server and receive confirmation
    comm.send_message(client_socket, "E " + ','.join(encrypt_data_list))
    message = comm.recieve_message(client_socket) # message not required. Only there for the flowstate of socket communication

def write(gui, fileName, selectedDir, selectedFile, cipher):
    with open(os.path.join(selectedDir, fileName + ".V"), "wb") as file:
        file.write(cipher)

    os.remove(selectedFile) # Deletes the file that was not encrypted
    gui.showMessage("File encrypted successfully.")


# Function to perform file encryption
def performEncryption(gui, comm, client_socket, selectedFile, encryptDialog, createNewName, saveInNewLocation, username, password):
    encryptDialog.destroy()
    try:
        # Gets the directory of the selected file if the value of saveInNewLocation is 0, otherwise executes pickDir function to get new location directory
        selectedDir = os.path.dirname(selectedFile) if not saveInNewLocation else gui.pickDir()

        # Get name of the file along with extension
        originalFileName = os.path.basename(selectedFile)

        # Generate a file ID to store for the database
        fileId = generateRandomKey()

        # Split the extension from the file name if createNewName value is 0, otherwise generate a random name, and attach to fileName variable
        fileName = os.path.splitext(originalFileName)[0] if not createNewName else generateRandomFileName()

        # Generate keyBytes to be used for encryption
        keyBytes = generateRandomKey()

        # Open the file to read and encrypt its contents with encryptByte function
        with open(selectedFile, "rb") as file:
            fileBytes = file.read()
        encryptedFileBytes, iv = encryptBytes(fileBytes, keyBytes)

        # Store cipher as encrypted fileID + encrypted content
        cipher = fileId + encryptedFileBytes

        # Create a message containing data to send to server
        sendkeys(comm, client_socket, fileId.hex(), originalFileName, keyBytes.hex(), iv.hex(), username, password)
        
        # Create file with .V extension in the provided directory to write and write the cipher onto it
        write(gui, fileName, selectedDir, selectedFile, cipher)

    except Exception as e:
        print(e)
        gui.showMessage("Error encrypting file.")