from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData
from sqlalchemy.orm import relationship

from database import Base

# metadata = MetaData()


class Role(Base):
    __tablename__ = "role"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True, nullable=False, unique=True)
    name = Column(String, nullable=False)
    permissions = Column(Integer, nullable=False)


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True, nullable=False, unique=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    bio = Column(String(200), nullable=True)
    avatar_id = Column(Integer, ForeignKey("files.id"), nullable=True)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    role_id = Column(Integer, ForeignKey("role.id"))
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
