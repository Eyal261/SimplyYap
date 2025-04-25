import secrets
import string

def generate_password(length: int):
    chars: str = string.ascii_letters + string.digits + string.punctuation
    password: str = ''.join(secrets.choice(chars) for _ in range(length))

    print(password)

#create and print a random number with up to 16 bits
#random = secrets.randbits(16)
#print(random)


#create and print a random token, with up to 32 bits
token = secrets.token_urlsafe(32)
print(token)



