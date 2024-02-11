# client.py (main)

from tkinter import BooleanVar, Toplevel, Checkbutton, Button
from gui import EncryptiVGUI
from communication import communication_with_ECDH
from authorize_user import login
from register import registerButtonClicked as register
from encrypt import performEncryption
from decrypt import performDecryption
import socket

# Choose file to Encrypt
def encryptFile():
    
    # Select file to Encrypt
    selectedFile = gui.pickFile()
    if selectedFile is None:
        return
    encryptDialog = Toplevel(gui.root)
    encryptDialog.title("Encryption Options")
    encryptDialog.geometry("300x150")

    createNewName = BooleanVar()
    saveInNewLocation = BooleanVar()

    # If clicked, createNewName value becomes 1 or True else 0 or False
    createNewNameCheckBox = Checkbutton(encryptDialog, text="Change File Name", variable=createNewName)
    # If clicked, saveInNewLocation value becomes 1 or True else 0 or False
    saveInNewLocationCheckBox = Checkbutton(encryptDialog, text="Save in New Location", variable=saveInNewLocation)

    # On clicking the button, selected file, dialog box, values of createNewName and saveInNewLocation get sent to performEncryption function
    encryptButton = Button(encryptDialog, text="Encrypt", command=lambda: performEncryption(gui, comm, client_socket, selectedFile, encryptDialog, createNewName.get(), saveInNewLocation.get(), gui.usernameField.get(), gui.passwordField.get()))
    
    # Destroys the dialog box
    cancelButton = Button(encryptDialog, text="Cancel", command=encryptDialog.destroy)

    createNewNameCheckBox.pack()
    saveInNewLocationCheckBox.pack()
    encryptButton.pack()
    cancelButton.pack()

# Choose file to decrypt
def decryptFile():
    
    # Pick file to decrypt
    selectedFile = gui.pickFile()
    if selectedFile is None:
        return
    
    # Read file
    with open(selectedFile, "rb") as file:
        cipher = file.read()
    
    # Perform decryption on file
    performDecryption(gui, comm, client_socket, gui.usernameField.get(), gui.passwordField.get(), selectedFile, cipher[:32], cipher[32:]) 
    
    
# Create a socket for the client
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:

    # Connect to the server
    client_socket.connect(("localhost", 12345))

    # Create an instance of gui
    gui = EncryptiVGUI()

    # Create an instance of communication
    comm = communication_with_ECDH(client_socket)

    # Give functionality to login and register buttons
    gui.loginButton.config(command = lambda: login(gui, comm, client_socket, gui.usernameField.get(), gui.passwordField.get()))
    gui.registerButton.config(command = lambda: register(gui, comm, client_socket, gui.usernameField.get(), gui.passwordField.get()))

    # Give functionality to encrypt and decrypt button
    gui.encryptFileButton.config(command = lambda: encryptFile())
    gui.decryptFileButton.config(command = lambda: decryptFile())


    # Run the tkinter window
    gui.run()




