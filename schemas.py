# Create the Pydantic models
# To avoid confusion between the SQLAlchemy models and the Pydantic models, 
# we will have the file models.py with the SQLAlchemy models, and the file schemas.py 
# with the Pydantic models.

# These Pydantic models define more or less a "schema" (a valid data shape).

# pydantic enforces type hints at runtime, and provides user friendly errors when data is invalid.
# Define how data should be in pure, canonical Python; validate it with pydantic.

from pydantic import BaseModel

# Create an CarBase and UserBase Pydantic models or just schemas 
# to have common attributes while creating or reading data.

class FileBase(BaseModel):
    file_name: str

class FileCreate(FileBase):
    pass

class File(FileBase):
    file_id: int
    user_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    login: str
    name: str
    surname: str
    city: str
    profession: str
    number: str
class UserCreate(UserBase):
    password: str

# will be used when reading data, when returning it from the API.
class User(UserBase):
    user_id: int
    user_files: list[File] = []

    class Config:
        orm_mode = True
