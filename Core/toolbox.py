from Core import models, serializers
import hashlib

def server_hash(data):
    """Generates a server-side hash using the SHA-256 algorithm."""
    
    hash = hashlib.sha256(data.encode()).hexdigest()

    return hash

def compare_hash(client_hash, server_hash):
    """Compares the server-side generated hash to the client-side hash."""

    if client_hash != server_hash:
        return False
    else:
        return True