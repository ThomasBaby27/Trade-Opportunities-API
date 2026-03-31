import jwt   # for JWT token
import os   # for environment variable management
from datetime import datetime, timedelta, timezone  # for handling token expiration
from fastapi import HTTPException, Security   # for handling HTTP exceptions and security dependencies
from fastapi.security import HTTPBearer   # for handling HTTP Bearer authentication
SECRET_KEY = os.getenv("SECRET_KEY", "appscrip_task_2026")   # Secret key for JWT
ALGORITHM = "HS256"  # Algorithm used for encoding and decoding JWT tokens
security = HTTPBearer()  # Initialize security for JWT authentication

# this function is for the create access token for the user.
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# this function is for the verify the JWT token for the user.
def verify_jwt(auth = Security(security)):
    token = auth.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")