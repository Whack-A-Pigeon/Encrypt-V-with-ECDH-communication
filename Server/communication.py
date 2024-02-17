# communication.py (server)

from aes256_gcm import encrypt, decrypt
import ecdh
from kyber1024 import Kyber
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class communication_with_ECDH:

    # Generate secret_shared_key
    def __init__(self, server_socket):

        # Generate ephemeral server keys
        self.kyber_public_key_server, self.kyber_secret_key_server = Kyber().keygen() # Kyber Key Generation
        self.ecdh_private_key_server, self.ecdh_public_key_server = ecdh.keygen() # ECDH Key Generation

        # Send the server's ephemeral public key to the client
        server_socket.sendall(self.ecdh_public_key_server)

        # Receive the client's ephemeral public key
        self.ecdh_public_key_client = server_socket.recv(1024)

        # Derive shared secret using ECDH
        self.ecdh_shared_secret = ecdh.derive_shared_secret(self.ecdh_private_key_server, self.ecdh_public_key_client) # Shared Secret Derivation
        self.shared_secret = self.hashed_secret(self.ecdh_shared_secret)

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

    def hashed_secret(self, secret):
        hasher = hashes.Hash(hashes.SHA256(), backend=default_backend())
        hasher.update(secret)
        return hasher.finalize()
