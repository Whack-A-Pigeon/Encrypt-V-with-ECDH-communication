# communications.py (client)

from aes256_gcm import encrypt, decrypt
import ecdh
from kyber1024 import Kyber
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class communication_with_ECDH:

    # Generate Shared Secret Key
    def __init__(self, client_socket):
        
        # Generate ephemeral client keys
        self.kyber_public_key_client, self.kyber_secret_key_client = Kyber().keygen() # Kyber Key Generation
        self.ecdh_private_key_client, self.ecdh_public_key_client = ecdh.keygen() # ECDH Key Generation

        # Send the client's ephemeral public key to the server
        client_socket.sendall(self.ecdh_public_key_client)

        # Receive the server's ephemeral public key
        self.ecdh_public_key_server = client_socket.recv(1024)

        # cipher_client, kyber_shared_secret_client = Kyber1024.enc(kyber_public_key_server) # Key Encapsulation

        # Derive shared secret using ECDH
        self.ecdh_shared_secret = ecdh.derive_shared_secret(self.ecdh_private_key_client, self.ecdh_public_key_server) # Shared Secret Derivation
        self.shared_secret = self.hashed_secret(self.ecdh_shared_secret)

        #send_message(client_socket, self.kyber_public_key_client)

        

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

    def hashed_secret(self, secret):
        hasher = hashes.Hash(hashes.SHA256(), backend=default_backend())
        hasher.update(secret)
        return hasher.finalize()