from routers.schemas import TestSuiteBase, TestSuiteUpdate
from sqlalchemy.orm.session import Session
from db.models import DbTestSuite, DbProject
import datetime
from fastapi import HTTPException, status


# Creating new Testsuite
def create_testsuite(db: Session, request: TestSuiteBase, current_user_id: int):
    new_testsuite = DbTestSuite(
        name = request.name,
        description = request.description,
        timestamp = datetime.datetime.now(),
        # project_id comes from -> schemas -> class TestSuiteBase(BaseModel) -> project_id: int
        project_id = request.project_id,
        # Due to we are passing the user who is logged, I think user_id is passed directly to -> models -> class DbTestSuite(Base): -> user_id = Column(Integer, ForeignKey('user.id'))
        user_id = current_user_id
    )
    db.add(new_testsuite)
    db.commit()
    db.refresh(new_testsuite)
    return new_testsuite


# Retrieving all the testsuites by project id, call this function on testsuite.py
def get_all_testsuites_by_project_id(db: Session, project_id: int):
    project = db.query(DbTestSuite).filter(DbTestSuite.project_id == project_id).all()

    # Exception in case the project id does not exist
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The project with id {project_id} does not exists')
    
    return project


# retrieving all the testsuites by project name
def get_all_testsuites_by_project_name(db: Session, project_name: str):
    project = db.query(DbProject).filter(DbProject.name.ilike(f"%{project_name}%")).first()

    # Exception in case the project does not exist
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The project with name {project_name} does not exists')

    testsuites = db.query(DbTestSuite).filter(DbTestSuite.project_id == project.id).all()
    return testsuites


# Update testsuite
def update_test_suite(db: Session, id: int, request: TestSuiteUpdate):
    test_suite = db.query(DbTestSuite).filter(DbTestSuite.id == id).first()

    # Exception in case the test suite does not exist
    if not test_suite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The test suite with id {id} does not exists')
    
    # if the project exists it will ipdate the the project information
    test_suite.name = request.name
    test_suite.description = request.description

    db.commit()

    return 'The test suite has been updated'


# Delete testsuite
def delete_test_suite(db: Session, id: int):
    test_suite = db.query(DbTestSuite).filter(DbTestSuite.id == id).first()

    # Exception in case the test suite does not exist
    if not test_suite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The test suite with id {id} does not exists')
    
    # Once passed the check
    db.delete(test_suite)
    db.commit()

    return 'Test suite has been deleted'
