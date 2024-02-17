from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec, padding
import os

# Function to generate a pair of ephemeral private and public keys using ECC
def keygen():
    private_key = ec.generate_private_key(ec.SECP521R1(), backend=default_backend())
    public_key = private_key.public_key()
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_key, public_key_bytes

# Function to derive a shared secret using ECDH and hash it with SHA-256
def derive_shared_secret(private_key, public_key_bytes):
    public_key = serialization.load_pem_public_key(public_key_bytes, backend=default_backend())
    shared_secret = private_key.exchange(ec.ECDH(), public_key)
    return shared_secret