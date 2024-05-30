from .database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


# creating user table
class DbUser(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    project_user = relationship('DbProject', back_populates='user_project')
    testsuite_user = relationship('DbTestSuite', back_populates='user_testsuite')
    testcase_user = relationship('DbTestCase', back_populates='user_testcase')


# creating project table
class DbProject(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))
    user_project = relationship('DbUser', back_populates='project_user')
    testsuite_project = relationship('DbTestSuite', back_populates='project_testsuite')


# creating test suite table
class DbTestSuite(Base):
    __tablename__ = 'testsuite'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    timestamp = Column(DateTime)
    project_id = Column(Integer, ForeignKey('project.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    project_testsuite = relationship('DbProject', back_populates='testsuite_project')
    testcase_testsuite = relationship('DbTestCase', back_populates='testsuite_testcase')
    user_testsuite = relationship('DbUser', back_populates='testsuite_user')


# creating test case table
class DbTestCase(Base):
    __tablename__ = 'testcase'
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String)
    title = Column(String)
    description = Column(String)
    priority = Column(String)
    type = Column(String)
    status = Column(String)
    precondition = Column(String)
    postcondition = Column(String)
    timestamp = Column(DateTime)
    testsuite_id = Column(Integer, ForeignKey('testsuite.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    testsuite_testcase = relationship('DbTestSuite', back_populates='testcase_testsuite')
    user_testcase = relationship('DbUser', back_populates='testcase_user')