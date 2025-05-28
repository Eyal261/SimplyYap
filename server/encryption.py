import secrets
import string

def generate_password(length: int):
    chars: str = string.ascii_letters + string.digits + string.punctuation
    password: str = ''.join(secrets.choice(chars) for _ in range(length))

    print(password)



