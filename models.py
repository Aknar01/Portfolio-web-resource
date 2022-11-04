# Create the database models

from sqlalchemy import Column, Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

## These are models taken from Lecture 7
# Nothing new here though 

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)  # integer primary key will be autoincremented by default
    login = Column(String(255), unique=True, nullable=False)
    name = Column(String(255))
    surname = Column(String(255))
    password = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    profession = Column(String(255), nullable=False)
    number = Column(String(255), nullable=False)
    user_files = relationship("File", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User(user_id {self.user_id!r}, name={self.name!r}, surname={self.surname!r})"


class File(Base):
    __tablename__ = "files"
    file_id = Column(Integer, primary_key=True)
    file_name = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    owner = relationship("User", back_populates="user_files")

    def __repr__(self) -> str:
        return f"Filer(file_id={self.file_id!r}, file_name={self.file_name!r}, owner={self.owner!r})"




