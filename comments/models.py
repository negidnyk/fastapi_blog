from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData
# from auth.models import user
from sqlalchemy.orm import relationship

from database import Base

metadata = MetaData()


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'))
    post_id = Column(Integer, ForeignKey("post.id", ondelete='CASCADE'))
    text = Column(String(500), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


# class PostComments(Base):
#     __tablename__ = "postComments"
#
#     id = Column(Integer, primary_key=True, index=True, nullable=False, unique=True)
#     post_id = Column(Integer, ForeignKey("post.id", ondelete='CASCADE'))
#     comment_id = Column(Integer, ForeignKey("comments.id", ondelete='CASCADE'))
