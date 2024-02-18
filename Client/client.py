import sys
import socket
from PyQt6.QtWidgets import QApplication, QDialog, QCheckBox, QPushButton, QMessageBox
from gui import EncryptiVGUI
from communication import Communication
from authorize_user import login
from register import registerButtonClicked as register
from encrypt import performEncryption
from decrypt import performDecryption

# Choose file to Encrypt
def encryptFile(window, comm, client_socket):
    selectedFile, _ = window.pickFile()
    if selectedFile:
        encryptDialog = QDialog(window)
        encryptDialog.setWindowTitle("Encryption Options")
        encryptDialog.setGeometry(100, 100, 300, 150)

        createNewName = QCheckBox("Change File Name", encryptDialog)
        saveInNewLocation = QCheckBox("Save in New Location", encryptDialog)

        encryptButton = QPushButton("Encrypt", encryptDialog)
        encryptButton.clicked.connect(lambda: performEncryption(window, comm, client_socket, selectedFile, encryptDialog, createNewName.isChecked(), saveInNewLocation.isChecked(), window.usernameField.text(), window.passwordField.text()))

        cancelButton = QPushButton("Cancel", encryptDialog)
        cancelButton.clicked.connect(encryptDialog.reject)

        createNewName.move(10, 10)
        saveInNewLocation.move(10, 40)
        encryptButton.move(50, 80)
        cancelButton.move(160, 80)

        encryptDialog.exec()

# Choose file to decrypt
def decryptFile(window, comm, client_socket):
    selectedFile, _ = window.pickFile()
    if selectedFile:
        try:
            with open(selectedFile, "rb") as file:
                cipher = file.read()
            performDecryption(window, comm, client_socket, window.usernameField.text(), window.passwordField.text(), selectedFile, cipher[:32], cipher[32:])
        except Exception as e:
            QMessageBox.critical(window, "Error", f"Error occurred while decrypting: {str(e)}")

# Create a socket for the client
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    try:
        # Connect to the server
        client_socket.connect(("localhost", 12345))

        # Create an instance of QApplication
        app = QApplication(sys.argv)

        # Create an instance of EncryptiVGUI
        window = EncryptiVGUI()

        # Create an instance of communication
        comm = Communication(client_socket)

        # Connect login and register buttons to functions
        window.loginButton.clicked.connect(lambda: login(window, comm, client_socket, window.usernameField.text(), window.passwordField.text()))
        window.registerButton.clicked.connect(lambda: register(window, comm, client_socket, window.usernameField.text(), window.passwordField.text()))

        # Connect encrypt and decrypt buttons to functions
        window.encryptFileButton.clicked.connect(lambda: encryptFile(window, comm, client_socket))
        window.decryptFileButton.clicked.connect(lambda: decryptFile(window, comm, client_socket))

        window.show()
        sys.exit(app.exec())

    except Exception as e:
        print(f"An error occurred: {e}")
