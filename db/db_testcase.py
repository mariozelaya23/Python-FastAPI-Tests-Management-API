import os
from routers.schemas import TestCaseBase, TestCaseUpdate
from sqlalchemy.orm.session import Session
from db.models import DbTestCase, DbTestSuite
import datetime
from fastapi import HTTPException, status


# Creating new Tescase
def create_testcase(db: Session, request: TestCaseBase, current_user_id: int, testsuite_id: int):
    
    # Check if testsuite_id exists
    testsuite = db.query(DbTestSuite).filter(DbTestSuite.id == testsuite_id).first()

    # Exception in case the test suite does not exist
    if not testsuite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The testsuite with id {testsuite_id} does not exists')

    new_testcase = DbTestCase(
        image_url = request.image_url,
        title = request.title,
        description = request.description,
        priority = request.priority,
        type = request.type,
        status = request.status,
        precondition = request.precondition,
        postcondition = request.postcondition,
        timestamp = datetime.datetime.now(),
        # testsuite_id comes from -> schemas -> class TestCaseBase(BaseModel) -> testsuite_id: int
        testsuite_id = request.testsuite_id,
        # Due to we are passing the user who is logged, I think this value is passed directly to: models -> class DbTestCase(Base): -> user_id = Column(Integer, ForeignKey('user.id'))
        user_id = current_user_id
    )
    db.add(new_testcase)
    db.commit()
    db.refresh(new_testcase)
    return new_testcase


# Retrieving all the testcases by testsuite id
def get_all_testcases_by_testsuite_id(db: Session, testsuite_id: int):
    testsuite = db.query(DbTestSuite).filter(DbTestSuite.id == testsuite_id).first()

    # Exception in case the test suite does not exist
    if not testsuite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The testsuite with id {testsuite_id} does not exists')
    
    testcases = db.query(DbTestCase).filter(DbTestCase.testsuite_id == testsuite.id).all()
    return testcases


# Retrieving all the testcases by testsuite
def get_all_testcases_by_testsuite_name(db: Session, testsuite_name: str):
    testsuite = db.query(DbTestSuite).filter(DbTestSuite.name.ilike(f"%{testsuite_name}%")).first()

    # Exception in case the project does not exist
    if not testsuite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The testsuite with name {testsuite_name} does not exists')

    testcases = db.query(DbTestCase).filter(DbTestCase.testsuite_id == testsuite.id).all()
    return testcases


# Update testcase
def update_test_case(db: Session, id: int, request: TestCaseUpdate):
    test_case = db.query(DbTestCase).filter(DbTestCase.id == id).first()

    # Exception in case the test suite does not exist
    if not test_case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The test case with id {id} does not exists')
    
    # if the testcase exists it will ipdate the the project information
    test_case.image_url = request.image_url
    test_case.title = request.title
    test_case.description = request.description
    test_case.priority = request.priority
    test_case.type = request.type
    test_case.status = request.status
    test_case.precondition = request.precondition
    test_case.postcondition = request.postcondition

    db.commit()

    return 'The test case has been updated'


# Delete Testcase
def delete_test_case(db: Session, id: int):
    test_case = db.query(DbTestCase).filter(DbTestCase.id == id).first()

    # Exception in case the test case does not exists
    if not test_case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The test case with id {id} does not exists')
    
    # Delete the image file if it exists
    if test_case.image_url and os.path.isfile(test_case.image_url):
        os.remove(test_case.image_url)
    
    # Once passed the check
    db.delete(test_case)
    db.commit()

    return 'Test case and associated image have been deleted'