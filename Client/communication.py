# communications.py (client)

from aes256_gcm import encrypt, decrypt
import ecdh
from kyber1024 import Kyber
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class Communication:

    # Generate Shared Secret Key
    def __init__(self, client_socket):
        
        # Generate client keys
        self.kyber_public_key_client, self.kyber_secret_key_client = Kyber().keygen() # Kyber Key Generation
        self.ecdh_private_key_client, self.ecdh_public_key_client = ecdh.keygen() # ECDH Key Generation

        # ECDH Public Key Exchange
        client_socket.sendall(self.ecdh_public_key_client)
        self.ecdh_public_key_server = client_socket.recv(1024)

        # Derive shared secret using ECDH
        self.ecdh_shared_secret = ecdh.derive_shared_secret(self.ecdh_private_key_client, self.ecdh_public_key_server)
        self.shared_secret = self.hashed_secret(self.ecdh_shared_secret)

        # Kyber Public Key Exchange
        self.send_message(client_socket, self.kyber_public_key_client, False)
        self.kyber_public_key_server = self.recieve_message(client_socket, False)
        

        # Kyber Key Encapsulation
        self.cipher_client, self.kyber_shared_secret_client = Kyber().enc(self.kyber_public_key_server)

        # Kyber Cipher Exchange
        self.send_message(client_socket, self.cipher_client, False)
        self.cipher_server = self.recieve_message(client_socket, False)

        # Kyber Key Decapsulation
        self.kyber_shared_secret_server = Kyber().dec(self.cipher_server, self.kyber_secret_key_client) 
        
        # Updating shared secret (ECDHE+Kyber)
        self.shared_secret = self.hashed_secret(self.ecdh_shared_secret + self.kyber_shared_secret_client + self.kyber_shared_secret_server)

    # Encrypt and send message to server
    def send_message(self, socket, message, string=True):        
        iv, tag, cipher = encrypt(self.shared_secret, message.encode() if string else message)
        encrypted_response = iv + tag + cipher
        socket.sendall(encrypted_response)

    # Decrypt and receive message from the server
    def recieve_message(self, socket, string=True):
        encrypted_message = socket.recv(4096)
        iv, tag, cipher = encrypted_message[:16], encrypted_message[16:32], encrypted_message[32:]
        decrypted_message = decrypt(self.shared_secret, iv, tag, cipher)

        return decrypted_message.decode() if string else decrypted_message

    def hashed_secret(self, secret):
        hasher = hashes.Hash(hashes.SHA256(), backend=default_backend())
        hasher.update(secret)
        return hasher.finalize()