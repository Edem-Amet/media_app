from jose import JWTError, jwt
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .database import get_db
from . import models


SECRET_KEY = "8e1e8be00f0b9a7617a6f724be66ba168c5ef013b83ea56324bfd941e92d4bce"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60



oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)



# Create JWT token
def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt




# Verify token
def verify_access_token(token: str, credentials_exception):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")


        if user_id is None:
            raise credentials_exception


    except JWTError:
        raise credentials_exception


    return user_id





# Get current logged-in user
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )


    user_id = verify_access_token(
        token,
        credentials_exception
    )


    user = (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .first()
    )


    if user is None:
        raise credentials_exception


    return user