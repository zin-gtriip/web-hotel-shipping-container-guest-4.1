import base64
from cryptography.fernet    import Fernet
from django.conf            import settings


def encrypt(text):
    """https://morioh.com/p/4f5288b77c14"""
    try:
        text = str(text) # convert integer etc to string first
        cipher_suite = Fernet(settings.FERNET_KEY) # get the key from settings, key should be byte
        encrypted_text = cipher_suite.encrypt(text.encode('ascii')) # input should be byte, so convert the text to byte
        encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode('ascii') # encode to urlsafe base64 format
        return encrypted_text
    except Exception as e:
        return None


def decrypt(text):
    """https://morioh.com/p/4f5288b77c14"""
    try:
        text = base64.urlsafe_b64decode(text) # base64 decode
        cipher_suite = Fernet(settings.FERNET_KEY) # get the key from settings, key should be byte
        decoded_text = cipher_suite.decrypt(text).decode('ascii') # decrypt and decode
        return decoded_text
    except Exception as e:
        return None
