from pydantic import BaseModel
from datetime import datetime


#----------------------USER----------------------

# Baseclass to send information tho the API
class UserBase(BaseModel):
    username: str
    email: str
    password: str


# What you show on the API
class UserDisplay(BaseModel):
    id: int
    username: str
    email: str
    class Config():
        orm_mode = True


#----------------------Project----------------------

# Baseclass to send information tho the API / These fields are going to appear at the endpoint
# Class to send information to the API when the user wants to modify a project, with this class you cannot modify the user ID on the project table
# the user id is taken from the get_current_user logged
class ProjectBase(BaseModel):
    name: str
    description: str
    #user_id: int


# To show the username who created the project on ProjectDisplay | "username" comes from -> model -> class DbUser(Base): nusername = Column(String), it has to be the same column name
class User(BaseModel):
    username: str
    class Config():
        orm_mode = True


#What you show on the API
class ProjectDisplay(BaseModel):
    id: int
    name: str
    description: str
    timestamp: datetime
    # user_project comes from models -> class DbProject(Base): -> user_project = relationship('DbUser', back_populates='project_user')
    user_project: User
    class Config():
        orm_mode = True


#----------------------User Authentication----------------------

# Data pass that requires authentication
class UserAuth(BaseModel):
    id: int
    username: str
    email: str


#----------------------TestSuite--------------------------------

# Baseclass to send information tho the API / These fields are going to appear at the endpoint
class TestSuiteBase(BaseModel):
    name: str
    description: str
    project_id: int


# To show the project name on TestSuiteDisplay | "name" comes from -> model -> class DbProject(Base): name = Column(String), it has to be the same column name
class Project(BaseModel):
    name: str
    class Config():
        orm_mode = True


# What you show on the API
class TestSuiteDisplay(BaseModel):
    id: int
    name: str
    description: str
    timestamp: datetime
    # project_testsuite comes from models -> DbTestSuite(Base): -> project_testsuite = relationship('DbProject', back_populates='testsuite_project')
    project_testsuite: Project
    # user_testsuite comes from models -> DbTestSuite(Base): user_testsuite = relationship('DbUser', back_populates='testsuite_user')
    user_testsuite: User
    class Config():
        orm_mode = True
    

# Update test suite class, these fields will be send to the API
class TestSuiteUpdate(BaseModel):
    name: str
    description: str


#----------------------TestCase--------------------------------

# Baseclass to send information tho the API / These fields are going to appear at the endpoint
class TestCaseBase(BaseModel):
    image_url: str
    title: str
    description: str
    priority: str
    type: str
    status: str
    precondition: str
    postcondition: str
    testsuite_id: int


# To show the testsuite name on TestCaseDisplay | "name" comes from -> model -> class DbTestSuite(Base): name = Column(String), it has to be the same column name
class TestSuite(BaseModel):
    name: str
    class Config():
        orm_mode = True


# What you show on the API
class TestCaseDisplay(BaseModel):
    id: int
    image_url: str
    title: str
    description: str
    priority: str
    type: str
    status: str
    precondition: str
    postcondition: str
    timestamp: datetime
    # testsuite_testcase comes from models -> class DbTestCase(Base): -> testsuite_testcase = relationship('DbTestSuite', back_populates='testcase_testsuite')
    testsuite_testcase: TestSuite
    # user_testcase comes from models -> class DbTestCase(Base): -> user_testcase = relationship('DbUser', back_populates='testcase_user') 
    user_testcase: User
    class Config():
        orm_mode = True


# Update test case class, these fields will be send to the API
class TestCaseUpdate(BaseModel):
    image_url: str
    title: str
    description: str
    priority: str
    type: str
    status: str
    precondition: str
    postcondition: str

