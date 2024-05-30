from routers.schemas import ProjectBase
from sqlalchemy.orm.session import Session
from db.models import DbProject
import datetime
from fastapi import HTTPException, status


# Creating new Project
def create_project(db: Session, request: ProjectBase, current_user_id: int):
    new_project = DbProject(
        name = request.name,
        description = request.description,
        timestamp = datetime.datetime.now(),
        # user_id comes from -> schemas -> class ProjectBase(BaseModel) -> user_id: int (we are not using this class anymore)
        # Due to we are passing the user who is logged, I think this value is passed directly to: models -> class DbProject(Base): -> user_id = Column(Integer, ForeignKey('user.id'))
        user_id = current_user_id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


# Retrieving all the pojects, call this function on project.py
def get_all_projects(db: Session):
    return db.query(DbProject).all()


# Retrieving project by project id
def get_project_by_project_id(db: Session, id: int):
    project = db.query(DbProject).filter(DbProject.id == id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Project with id {id} does not exist')
    return project


# Retrieving project by project name CASE INSENSITIVE
def get_project_by_project_name(db: Session, name: str):
    projects = db.query(DbProject).filter(DbProject.name.ilike(f"%{name}%")).all()
    if not projects:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No projects found with the name {name}')
    return projects


# Update the project
def update_project(db: Session, id: int, request: ProjectBase, current_user_id: int):

    project = db.query(DbProject).filter(DbProject.id == id).first()

    # exception in case the project does not exist
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The Project with id {id} not found')
    
    # check if the project belongs to the current user
    if project.user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not authorized to update this project, you can only update projects that belongs to you')
    
    # if the project is found it will update the project information
    project.name = request.name
    project.description = request.description
    #project.user_id = request.user_id

    db.commit()

    return "The project has been updated"


# Update all project field, including the user id 
# def update_project_all(db: Session, id: int, request: ProjectBase):

#     project = db.query(DbProject).filter(DbProject.id == id).first()
    
#     # exception in case the project does not exist
#     if not project:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The Project with id {id} not found')
    
#     # If the project exists
#     project.name = request.name
#     project.description = request.description
#     project.user_id = request.user_id

#     db.commit()

#     return "The project has benn updated"


# Delete a project
def delete_project(db: Session, id: int, current_user_id: int):

    project = db.query(DbProject).filter(DbProject.id == id).first()

    # exception in case the project does not exist
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The Project with id {id} not found')
    
    # check if the project belongs to the current user
    if project.user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not authorized to delete this project, you can only delete the projects that belongs to you')
    
    # Once passed all checks
    db.delete(project)

    db.commit()
    
    return 'Project deleted'