# Show user endpoint on the API Docs
from fastapi import APIRouter, Depends, status
from routers.schemas import ProjectBase, ProjectDisplay
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_project
from typing import List
import random
import string
import shutil
from routers.schemas import UserAuth
from auth.oauth2 import get_current_user


# Creating router
router = APIRouter(
    prefix='/project',
    tags=['project']
)


# Creating a new project
# to add authentication for this method, add: current_user: UserAuth = Depends(get_current_user) in definition
@router.post('', response_model=ProjectDisplay)
def create_project(request: ProjectBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_project.create_project(db, request, current_user.id)


# Retrieving all the projects
@router.get('/all', response_model=List[ProjectDisplay])
def get_all_projects(db: Session = Depends(get_db)):
    return db_project.get_all_projects(db)


# Retrieving the project by project id
@router.get('/{id}', response_model=ProjectDisplay)
def get_project_by_project_id(id: int, db: Session = Depends(get_db)):
    return db_project.get_project_by_project_id(db, id)


# Retrieving the project by project name CASE INSENSITIVE
@router.get('/projectname/{name}', response_model=List[ProjectDisplay])
def get_project_by_project_name(name: str, db: Session = Depends(get_db)):
    return db_project.get_project_by_project_name(db, name)


# Endpoint updating a project
@router.put('/{id}')
def update_project(id: int, request: ProjectBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_project.update_project(db, id, request, current_user.id)


# Endpoint updating all project fields
# @router.put('/{id}')
# def update_project_all(id: int, request: ProjectBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
#     return db_project.update_project_all(db, id, request)


# Endpoint deleting a project
@router.delete('/{id}')
def delete_project(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_project.delete_project(db, id, current_user.id)