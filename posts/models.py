from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData
# from auth.models import user
from sqlalchemy.orm import relationship

from database import Base

metadata = MetaData()


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True, nullable=False, unique=True)
    title = Column(String(150), nullable=False)
    description = Column(String(1500))
    creator_id = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # user = relationship('User', back_populates='posts')
    # postLikes = relationship('PostLikes', back_populates='post', cascade='all, delete-orphan')
    # userPost = relationship('UserPost', back_populates='post', cascade='all, delete-orphan')

class PostLikes(Base):
    __tablename__ = "postLikes"

    id = Column(Integer, primary_key=True, index=True, nullable=False, unique=True)
    post_id = Column(Integer, ForeignKey("post.id", ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'))

    # post = relationship('Post', back_populates='postLikes')
    # user = relationship('User', back_populates='postLikes')

class UserPost(Base):
    __tablename__ = "user_post"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    post_id = Column(Integer, ForeignKey("post.id", ondelete='CASCADE'))
    creator_id = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'))

    # post = relationship('Post', back_populates='userPost')
    # user = relationship('User', back_populates='userPost')





