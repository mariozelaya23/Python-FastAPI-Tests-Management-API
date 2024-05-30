# Show user endpoint on the API Docs
from fastapi import APIRouter, Depends
from routers.schemas import TestSuiteBase, TestSuiteDisplay, TestSuiteUpdate
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_testsuite
from typing import List
from routers.schemas import UserAuth
from auth.oauth2 import get_current_user


# Creating router
router = APIRouter(
    prefix='/testsuite',
    tags=['testsuite']
)


# Creating a new testsuite
# to add authentication for this method, add: current_user: UserAuth = Depends(get_current_user) in definition
@router.post('', response_model=TestSuiteDisplay)
def create_testsuite(request: TestSuiteBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_testsuite.create_testsuite(db, request, current_user.id)


# Retrieving all the testsuites by project id
@router.get('/{project_id}', response_model=List[TestSuiteDisplay])
def get_all_testsuites_by_project_id(project_id: int, db: Session = Depends(get_db)):
    return db_testsuite.get_all_testsuites_by_project_id(db, project_id)


# Retrieving all the testsuites by project name
@router.get('/project/{project_name}', response_model=List[TestSuiteDisplay])
def get_all_testsuites_by_project_name(project_name: str, db: Session = Depends(get_db)):
    return db_testsuite.get_all_testsuites_by_project_name(db, project_name)


# Endpoint updating a test suite
@router.put('/{id}')
def update_testsuite(id: int, request: TestSuiteUpdate, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_testsuite.update_test_suite(db, id, request)


# Endpoint deleting a test suite
@router.delete('/{id}')
def delete_testsuite(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_testsuite.delete_test_suite(db, id)