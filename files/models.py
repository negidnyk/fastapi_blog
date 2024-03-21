from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData
from sqlalchemy.orm import relationship

from database import Base

metadata = MetaData()


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True, nullable=False, unique=True)
    file = Column(String(1000), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'))
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    is_used = Column(Boolean, default=False, nullable=False)






