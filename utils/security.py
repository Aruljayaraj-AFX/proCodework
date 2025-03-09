import os
from jose import jwt
from dotenv import load_dotenv
import string
import random

load_dotenv()
token_expiry_minutes = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
algorithm = os.getenv('ALGORITHM')
secret_key = os.getenv('JWT_SECRET_KEY')
db_url = os.getenv('DB_URL')

def hashword(password):
    return jwt.encode({"password":password}, secret_key , algorithm=algorithm)

def decode(password):
    return jwt.decode(password,secret_key, algorithms=[algorithm])
