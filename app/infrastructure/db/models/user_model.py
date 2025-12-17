from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import declarative_base

from app.core.enums.user_role import UserRole

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.MEMBER)
