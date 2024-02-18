from communication import Communication
from database import connectToDatabase
from checkLogin import Authorize
from registration import registerUser
from storeKey import storeKeyInDatabase
from decryptProcess import getKeyFromDatabase, deleteRecord
import socket
import threading

# Function to handle each client connection
def handle_client(client_socket, address, connection):
    # Intialize comms object
    comm = Communication(client_socket)
    
    try:
        while True:
            # Receive message from client
            received_message = comm.receive_message(client_socket)
            
            if not received_message:
                break
            
            # Login Check
            if received_message[0] == 'L':
                # Separate received_message to username and password
                received_message = received_message[2:].split(',')
                user_id = Authorize(connection, received_message[0], received_message[1])
                # Message user_id to send to client
                message = str(user_id)
                
            # Register User
            elif received_message[0] == 'R':
                # Separate received_message to username and password
                received_message = received_message[2:].split(',')
                username, password = received_message[0], received_message[1]
                # It takes the user data and registers to database 
                if registerUser(connection, username, password):
                    message = "registered"
                    
            # Encrypted Details Storage
            elif received_message[0] == 'E':
                # Store key and metadata into the database
                storeKeyInDatabase(received_message[2:], connection)
                # Send message that key is stored
                message = "stored"
                
            # Data for decryption
            elif received_message[0] == 'D':
                # Get key and metadata from the database
                details = getKeyFromDatabase(received_message[2:], connection)
                # Send the metadata to the client
                message = ','.join(details)
                    
            # Delete record
            elif received_message[0] == 'O':
                deleteRecord(received_message[2:], connection)
                message = "lmao"
                
            # Send message to client
            comm.send_message(client_socket, message)
    except Exception as e:
        print(f"Error handling client {address}: {e}")
    finally:
        # Close the client socket
        client_socket.close()
        print(f"Closed connection with {address}")

# Main function to run the server
def main():
    # Create an instance of the database
    connection = connectToDatabase()
    
    # Create a socket for the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind the socket to an IP address and port
        server_socket.bind(("localhost", 12345))
        
        # Listen for incoming connections
        server_socket.listen()
        
        print("Server is listening for connections...")
        
        try:
            while True:
                # Accept a connection from a client
                client_socket, addr = server_socket.accept()
                print(f"Accepted connection from {addr}")
                
                # Create a new thread to handle the client
                client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, connection))
                client_thread.start()
        except KeyboardInterrupt:
            print("Server shutting down...")

if __name__ == "__main__":
    main()
