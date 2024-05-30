from routers.schemas import UserBase
from sqlalchemy.orm.session import Session
from db.models import DbUser
from db.hashing import Hash
from fastapi import HTTPException, status


# Create a user in the DB
def create_user(db: Session, request: UserBase):
    # DbUser -> models.py
    new_user = DbUser(
        username = request.username,
        email = request.email,
        password = Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Retrieving all the users, call this function on user.py
def get_all_users(db: Session):
    return db.query(DbUser).all()


# Retrieve user by user id
def get_user_by_user_id(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')
    return user


# Retrieving user by username, this function will be use it by oauth.py -> in -> def get_current_user, this function is use for authentication purposes
def get_user_by_username(db: Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with username {username} not found')
    return user


# Retrieving user by username
def get_user_by_username_case_insensitive(db: Session, username: str):
    users = db.query(DbUser).filter(DbUser.username.ilike(f"%{username}%")).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No users found with the username {username}')
    return users


# Update the user
def update_user(db: Session, id: int, request: UserBase):
    user = db.query(DbUser).filter(DbUser.id == id).first()

    # exception in case the user does not exist
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')
    
    # if the user is found it will update the user information
    user.username = request.username
    user.email = request.email
    user.password = Hash.bcrypt(request.password)
    db.commit()

    return 'The user has been updated'
    

# Delete user
def delete_user(db: Session, id: int, user_id: int):
    
    # Exception in case the user tries to delete themselves
    if id == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You cannot delete your own account')

    user = db.query(DbUser).filter(DbUser.id == id).first()
    
    # exception in case the user is not found
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')

    # Once passed all checks
    db.delete(user)
    db.commit()
    return 'User deleted'