#import jwt
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings



# SECRET_KEY
# Algorithm
# Expriation time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# def verify_access_token(token: str):

#     try:

#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         print (payload)
#         username: str = payload.get("sub")
#         print(username)
#         if username is None:
#             return None
#         return username
#         #token_data = schemas.TokenData(use=username)
#         print(token_data)
#         #return username
#     except jwt.PyJWTError:
#         return None

#     return token_data

def verify_access_token(token: str, credentials_exception):

    try:
        print(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print (payload)
        id: str = payload.get("user_id")
        print(id)
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
        print(token_data)
        #return username
    except JWTError:
        raise credentials_exception

    return token_data

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                           detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    # Get current User JWT token
    #username = verify_access_token(token, credentials_exception)
    token = verify_access_token(token, credentials_exception)
    #print(username)
    print(token)
    # if username is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid authentication credentials",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
   # user = db.query(models.User).filter(models.User.email == username).first()
    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    print(user)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user