from fastapi import APIRouter, Depends, status, UploadFile, File
from routers.schemas import TestCaseBase, TestCaseDisplay, TestCaseUpdate
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_testcase
from typing import List
import random
import string
import shutil
from routers.schemas import UserAuth
from auth.oauth2 import get_current_user


# Creating router
router = APIRouter(
    prefix='/testcase',
    tags=['testcase']
)


# Creating a new testcase
# to add authentication for this method, add: current_user: UserAuth = Depends(get_current_user) in definition
@router.post('', response_model=TestCaseDisplay)
def create_testcase(request: TestCaseBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_testcase.create_testcase(db, request, current_user.id, request.testsuite_id)


# Retrieving all the testcases by testsuite id
@router.get('/{testsuite_id}', response_model=List[TestCaseDisplay])
def get_all_testcases_by_testsuite_id(testsuite_id: int, db: Session = Depends(get_db)):
    return db_testcase.get_all_testcases_by_testsuite_id(db, testsuite_id)


# Retrieving all the testcases by testsuite name
@router.get('/testsuite/{testsuite_name}', response_model=List[TestCaseDisplay])
def get_all_testcases_by_testsuite_name(testsuite_name: str, db: Session = Depends(get_db)):
    return db_testcase.get_all_testcases_by_testsuite_name(db, testsuite_name)


# Endpoint updating a test case
@router.put('/{id}')
def update_testcase(id: int, request: TestCaseUpdate, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_testcase.update_test_case(db, id, request)


# Endpoint deleting a test case
@router.delete('/{id}')
def delete_testcase(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return db_testcase.delete_test_case(db, id)


# Upload images from the PC
@router.post('/image')
def upload_image(image: UploadFile = File(...)):
    letters = string.ascii_letters
    rand_str = ''.join(random.choice(letters) for i in range(6))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.',1))
    path = f'images/{filename}'

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    return {'filename': path}
