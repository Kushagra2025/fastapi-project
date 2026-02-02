from fastapi import APIRouter, Depends, HTPException, status, Response
from sqlalchemy.orm import Session
from .. import database, schemas, models

router = APIRouter(tags=["Authentication"])

@router.post('/login')
def login(user_credential: schemas.UserLogin, db: Session = Depends(database.get_db)):

    db.query(models.User)
