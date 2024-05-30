# Show user endpoint on the API Docs
from fastapi import APIRouter, Depends
from routers.schemas import UserBase, UserDisplay
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_user
from typing import List
from routers.schemas import UserAuth
from auth.oauth2 import get_current_user


# Creating router
router = APIRouter(
    prefix='/user',
    tags=['user']
)


# Creating a new user
@router.post('', response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)


# Retrieving all the users
# to add authentication for this method, add: current_user: UserAuth = Depends(get_current_user) in definition
@router.get('/all', response_model=list[UserDisplay])
def get_all_users(db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_user.get_all_users(db)


# Retrive the user by user id
@router.get('/{id}', response_model=UserDisplay)
def get_user_by_user_id(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_user.get_user_by_user_id(db, id)


# Retrive the user by username CASE INSENSITIVE
@router.get('/username/{username}', response_model=List[UserDisplay])
def get_user_by_username(username: str, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_user.get_user_by_username_case_insensitive(db, username)


# Endpoint updating the user
@router.put('/{id}')
def update_user(id: int, request: UserBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_user.update_user(db, id, request)


# Endpoint deleting a user
@router.delete('/{id}')
def delete_user(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_user.delete_user(db, id, current_user.id)