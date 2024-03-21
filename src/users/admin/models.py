# from datetime import datetime
# from sqlalchemy import MetaData
# from sqlalchemy import TIMESTAMP
# from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship
# from database import Base
#
#
# metadata = MetaData()
#
# class Role(Base):
#     __tablename__ = "role"
#
#     id = Column(Integer, primary_key=True, index=True)
#     role = Column(String, unique=True)
#
#     users = relationship("User", back_populates="role")
#
#
# class User(Base):
#     __tablename__ = "user"
#
#     id = Column(Integer, primary_key=True, index=True, nullable=False, unique=True)
#     email = Column(String, unique=True, index=True, nullable=False)
#     username = Column(String)
#     hashed_password = Column(String, nullable=False)
#     is_active = Column(Boolean, default=True, nullable=False)
#     is_superuser = Column(Boolean, default=False, nullable=False)
#     is_verified = Column(Boolean, default=False, nullable=False)
#     registered_at = Column(TIMESTAMP, default=datetime.utcnow)
#     role = Column(Integer, ForeignKey(Role.id))
#
#     roles = relationship("Role", back_populates="user")
