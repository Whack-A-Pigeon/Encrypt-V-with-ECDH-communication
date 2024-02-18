# communication.py (server)

from aes256_gcm import encrypt, decrypt
import ecdh
from kyber1024 import Kyber
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class Communication:

    # Generate secret_shared_key
    def __init__(self, server_socket):

        # Generate server keys
        self.kyber_public_key_server, self.kyber_secret_key_server = Kyber().keygen() # Kyber Key Generation
        self.ecdh_private_key_server, self.ecdh_public_key_server = ecdh.keygen() # ECDH Key Generation

        # ECDH Public Key Exchange
        server_socket.sendall(self.ecdh_public_key_server)
        self.ecdh_public_key_client = server_socket.recv(1024)

        # Derive shared secret using ECDH
        self.ecdh_shared_secret = ecdh.derive_shared_secret(self.ecdh_private_key_server, self.ecdh_public_key_client)
        self.shared_secret = self.hashed_secret(self.ecdh_shared_secret)

        # Kyber Public Key Exchange
        self.send_message(server_socket, self.kyber_public_key_server, False)
        self.kyber_public_key_client = self.receive_message(server_socket, False)

        # Kyber Key Encapsulation
        self.cipher_server, self.kyber_shared_secret_server = Kyber().enc(self.kyber_public_key_client)

        # Kyber Cipher Exchange
        self.send_message(server_socket, self.cipher_server, False)
        self.cipher_client = self.receive_message(server_socket, False)

        # Kyber Key Decapsulation
        self.kyber_shared_secret_client = Kyber().dec(self.cipher_client, self.kyber_secret_key_server)
        
        # Updating shared secret (ECDHE+Kyber)
        self.shared_secret = self.hashed_secret(self.ecdh_shared_secret + self.kyber_shared_secret_client + self.kyber_shared_secret_server)

    # Function to encrypt and send message to client
    def send_message(self, socket, message, string=True):        
        iv, tag, cipher = encrypt(self.shared_secret, message.encode() if string else message)
        encrypted_response = iv + tag + cipher
        socket.sendall(encrypted_response)

    # Function to receive and decrypt message from client
    def receive_message(self, socket, string=True):
        encrypted_message = socket.recv(4096)
        iv, tag, cipher = encrypted_message[:16], encrypted_message[16:32], encrypted_message[32:]
        decrypted_message = decrypt(self.shared_secret, iv, tag, cipher)

        return decrypted_message.decode() if string else decrypted_message

    def hashed_secret(self, secret):
        hasher = hashes.Hash(hashes.SHA256(), backend=default_backend())
        hasher.update(secret)
        return hasher.finalize()
