from website.flaskapp import db


class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)  # integer primary key will be autoincremented by default
    login = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    password = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    profession = db.Column(db.String(255), nullable=False)
    number = db.Column(db.String(255), nullable=False)
    user_files = db.relationship("File", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User(user_id {self.user_id!r}, name={self.name!r}, surname={self.surname!r})"


class File(db.Model):
    __tablename__ = "files"
    file_id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    owner = db.relationship("User", back_populates="user_files")