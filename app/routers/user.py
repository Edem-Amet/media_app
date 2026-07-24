from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas, utils, oauth2


router = APIRouter(
    tags=["user"]
)



# ==========================
# Create User
# ==========================

@router.post(
    "/create_user",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserOut
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    hashed_password = utils.hash(user.password)


    new_user = models.User(
        email=user.email,
        password=hashed_password
    )


    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return new_user

