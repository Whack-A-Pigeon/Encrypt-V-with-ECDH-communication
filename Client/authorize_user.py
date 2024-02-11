# authorize_user.py
# Used for login and retrieving userID

# Retrieve UserID
def authorize(comm, client_socket, username, password):

    # Send username and password to server to check
    comm.send_message(client_socket, "L " + username + "," + password)

    # Recieve authorization
    return comm.recieve_message(client_socket)

# Login Procedure
def login(gui, comm, client_socket, username, password):

    # Authorize user
    user_id = authorize(comm, client_socket, username, password)

    # If userID not valid
    if user_id == '-1':
        gui.showMessage("Login failed. Invalid username or password.")

    # If userId is valid, then show the Encrypt and Decrypt page
    else:
        gui.hideComponents(2)
        gui.showButtons()