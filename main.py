# Main FastAPI app

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

from fastapi.middleware.wsgi import WSGIMiddleware
from website.flask_main import app

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# craete fastapi (app) instance
fapp = FastAPI()

# need to have an independent database session/connection
# this function lets us to use the same connection throughout request lifecycle
# to accomplish the task above we will use this function as dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    # even if we catch an error the connection is gonna be closed
    finally:
        db.close()

# Depends here is needed to share database connections
@fapp.post("/api/users/create", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = crud.get_user_by_login(db, user_login=user.login)

    if new_user:
        raise HTTPException(status_code=400, detail="Login is already taken by another user. Use another, dattebayo.")
    return crud.create_user(db=db, user=user)

# creating a new car 
@fapp.post("/api/files", response_model=schemas.File)
def create_file(user_id:int, file: schemas.FileCreate, db: Session=Depends(get_db)):
    return crud.create_file(user_id=user_id, db=db, file=file)

# getting all users and their cars actually because of back populates
@fapp.get("/api/users", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_all_users(db)
    return users

# getting user(s) by their first name
@fapp.get("/api/users/fname/{user_fname}", response_model=list[schemas.User])
def get_users_by_name(user_fname, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_user_by_fname(db=db, user_fname=user_fname)
    return users

# getting a user with a specific login which is unique
@fapp.get("/api/users/{login}", response_model=schemas.User)
def get_certain_user(login, db: Session = Depends(get_db)):
    return crud.get_user_by_login(db, login)

# getting all cars from db
@fapp.get("/api/file/{user_id}", response_model=list[schemas.File])
def get_files_by_user_id(user_id, db: Session = Depends(get_db)):
    return crud.get_files_by_user_id(db, user_id)

# getting a specific user's cars
@fapp.get("/api/user/files/{user_id}", response_model=list[schemas.File])
def get_user_files(user_id, db: Session = Depends(get_db)):
    return crud.get_user_files(db, user_id)

# getting a certain car by its id
@fapp.get("/api/file/{file_id}/", response_model=schemas.File)
def get_file(file_id:int, db: Session = Depends(get_db)):
    return crud.get_file_by_id(db, file_id)


fapp.mount("/", WSGIMiddleware(app))
