# communication.py (server)

from ecdh import generate_ephemeral_key, serialize_key, deserialize_key, derive_shared_secret, encrypt, decrypt

class communication_with_ECDH:

    # Generate secret_shared_key
    def __init__(self, server_socket):
        # Generate ephemeral server keys
        self.server_ephemeral_private_key, self.server_ephemeral_public_key = generate_ephemeral_key()

        # Send the server's ephemeral public key to the client
        server_socket.sendall(serialize_key(self.server_ephemeral_public_key))

        # Receive the client's ephemeral public key
        self.client_ephemeral_public_key_data = server_socket.recv(1024)
        self.client_ephemeral_public_key = deserialize_key(self.client_ephemeral_public_key_data)

        # Derive shared secret using ECDH
        self.shared_secret = derive_shared_secret(self.server_ephemeral_private_key, self.client_ephemeral_public_key)

    # Function to encrypt and send message to client
    def send_message(self, server_socket, message):
        iv, tag, cipher = encrypt(self.shared_secret, message.encode())
        encrypted_response = iv + tag + cipher
        server_socket.sendall(encrypted_response)

    # Function to recieve and decrypt message from client
    def recieve_message(self, server_socket):
        
        encrypted_message = server_socket.recv(1024)
        iv, tag, cipher = encrypted_message[:16], encrypted_message[16:32], encrypted_message[32:]
        decrypted_message = decrypt(self.shared_secret, iv, tag, cipher)

        return decrypted_message.decode()
