from sqlalchemy import Column, String, Integer, DateTime

from src.config.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    password = Column(String, nullable=False)
    confirm_password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")
    branch = Column(String, nullable=False)
    phone = Column(String, nullable=False, index=True)
    address = Column(String, nullable=False)
    image = Column(String, nullable=False)
    status = Column(String, nullable=False, default="Active")
    deleted_at = Column(DateTime, nullable=True)
