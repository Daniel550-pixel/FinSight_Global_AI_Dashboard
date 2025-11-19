from cryptography.fernet import Fernet
KEY = Fernet.generate_key()
cipher = Fernet(KEY)
def encrypt(data: str) -> bytes:
    return cipher.encrypt(data.encode())
def decrypt(token: bytes) -> str:
    return cipher.decrypt(token).decode()
