# server.py (main)

from communication import communication_with_ECDH
from database import connectToDatabase
from checkLogin import Authorize
from registration import registerUser
from storeKey import storeKeyInDatabase
from decryptProcess import getKeyFromDatabase, deleteRecord
import socket

# Create an instance of database
connection = connectToDatabase()

# Create a socket for the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

    # Bind the socket to an IP address and port
    server_socket.bind(("localhost", 12345))
    
    # Listen for incoming connections
    server_socket.listen()

    # Accept a connection from a client
    server_socket, addr = server_socket.accept()

    with server_socket:

        # Intialize comms object
        comm = communication_with_ECDH(server_socket)

        while True:

            # Recieve message from client
            received_message = comm.recieve_message(server_socket)
        
            # Login Check
            if received_message[0] == 'L':

                # Separate received_message to username and password
                received_message = received_message[2:].split(',')
                user_id = Authorize(connection, received_message[0], received_message[1])

                # Message user_id to send to client
                message = str(user_id)

            # Register User
            if received_message[0] == 'R':

                # Separate received_message to username and password
                received_message = received_message[2:].split(',')
                username, password = received_message[0], received_message[1]

                # It takes the user data and registers to database 
                if registerUser(connection, username, password):
                    message = "registered"
            
            # Encrypted Details Storage
            if received_message[0] == 'E':

                # Store key and metadata into database
                storeKeyInDatabase(received_message[2:], connection)

                # Send message that key is stored
                message = "stored"

            # Data for decryption
            if received_message[0] == 'D':

                # Get key and metadata from database
                details = getKeyFromDatabase(received_message[2:], connection)

                # Send the metadata to client
                message = ','.join(details)
            
            # Delete record
            if received_message[0] == 'O':
                deleteRecord(received_message[2:], connection)
                message = "lmao"

            # Send message to client
            comm.send_message(server_socket, message)