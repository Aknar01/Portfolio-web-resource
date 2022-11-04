# CReateUpdateDelete utils (CRUD)
# reusable functions to interact with the data in the database.

from sqlalchemy.orm import Session
import models, schemas

# getting a user by login from a query to Users table using SQLAlchemy model User
def get_user_by_login(db: Session, user_login: int)->Session.query:
    return db.query(models.User).filter(models.User.login == user_login).first()

# getting a user by fname from a query to Users table using SQLAlchemy model User
# returns a list of user objects as a query
def get_user_by_fname(db: Session, user_fname: str)->Session.query:
    return db.query(models.User).filter(models.User.name == user_fname).all()

# getting all users from a query to Users table using SQLAlchemy model User
def get_all_users(db: Session, skip: int = 0, limit: int = 100)->Session.query:
    return db.query(models.User).offset(skip).limit(limit).all()

# getting a car by a car_id field 
def get_file_by_id(db: Session, file_id: int)->Session.query:
    return db.query(models.File).filter(models.File.file_id == file_id).first()

# getting a user cars
def get_user_files(db: Session, user_id: int)->Session.query:
    return db.query(models.File).filter(models.File.user_id == user_id).all()

# getting all cars
def get_files_by_user_id(db: Session, user_id:int)->Session.query:
    return db.query(models.File).filter(models.File.user_id == user_id).all()

# creating a user from instance of UserCreate
def create_user(db: Session, user: schemas.UserCreate)->models.User:
    new_user = models.User(login=user.login, 
                            name=user.name,
                            user_sname=user.surname,
                            password=user.password)
    # new_user = models.User(**user.dict()) # this is actually the same as above
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def create_file(db: Session, file: schemas.FileCreate, user_id)->models.File:
    new_file = models.File(file_name=file.file_name,
                            user_id=user_id)
    
    # new_file = models.File(**file.dict(), user_id=user_id)
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file



