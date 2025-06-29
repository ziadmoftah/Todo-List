from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=['bcrypt'] , deprecated='auto')
# helper functions
def hash(password: str) -> str:
    return bcrypt_context.hash(password)

def verify(plain_password: str , hashed_password : str) -> bool:
    return bcrypt_context.verify(plain_password , hashed_password)