# register.py

import re

# Function to check if a password is strong
def isStrongPassword(password):
    return password is not None and re.match("^(?=.*[A-Z])(?=.*[a-z])(?=.*\\d)(?=.*[_@#$%^&+=!]).{8,}$", password)

# Function for when register button is clicked
def registerButtonClicked(gui, comm, client_socket, username, password):
    
    # Check if username or password is entered
    if username is None or password is None:
        gui.showMessage("Enter a Valid Username and password.")
    
    # Check if the password is strong
    elif isStrongPassword(password):

        # Encrypt and send username and password to server to add to database
        comm.send_message(client_socket, "R " + username + "," + password)

        # Recieve confirmation of registration from user
        if comm.recieve_message(client_socket) == 'registered':
            gui.showMessage("Registration successful. You can now log in")
    
    # The password is not strong
    else:
        gui.showMessage("Enter a Strong password.")
    return False