# communications.py (client)

from ecdh import generate_ephemeral_key, serialize_key, deserialize_key, derive_shared_secret, encrypt, decrypt

class communication_with_ECDH:

    # Generate Shared Secret Key
    def __init__(self, client_socket):
        
        # Generate ephemeral client keys
        self.client_ephemeral_private_key, self.client_ephemeral_public_key = generate_ephemeral_key()

        # Client Socket
        self.client_socket = client_socket

        # Send the client's ephemeral public key to the server
        client_socket.sendall(serialize_key(self.client_ephemeral_public_key))

        # Receive the server's ephemeral public key
        self.server_ephemeral_public_key_data = client_socket.recv(1024)
        self.server_ephemeral_public_key = deserialize_key(self.server_ephemeral_public_key_data)

        # Derive shared secret using ECDH
        self.shared_secret = derive_shared_secret(self.client_ephemeral_private_key, self.server_ephemeral_public_key)

    # Encrypt and send message to server
    def send_message(self, client_socket, message):
        
        iv, tag, cipher = encrypt(self.shared_secret, message.encode())
        encrypted_response = iv + tag + cipher
        client_socket.sendall(encrypted_response)

    # Decrypt and receive message from the server
    def recieve_message(self, client_socket):

        encrypted_message = client_socket.recv(1024)
        iv, tag, cipher = encrypted_message[:16], encrypted_message[16:32], encrypted_message[32:]
        decrypted_message = decrypt(self.shared_secret, iv, tag, cipher)

        return decrypted_message.decode()