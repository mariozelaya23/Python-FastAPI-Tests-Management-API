from fastapi import FastAPI
# generate models, from models.py
from db import models
from db.database import engine
from routers import user, project, testsuite, testcase
from auth import authentication
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


#adding routers
app.include_router(user.router)
app.include_router(project.router)
app.include_router(testsuite.router)
app.include_router(testcase.router)
app.include_router(authentication.router)


@app.get("/")
def root():
    return 'Hello'


# defining array of places that are allow to connect from, javascript application runs in port 3000
origins = [
    'http://localhost:3000'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

models.Base.metadata.create_all(engine)

# Making image folder accessible statically
app.mount('/images', StaticFiles(directory='images'), name='images')

