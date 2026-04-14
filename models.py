from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship

from database import Base

class SchedulesNew(Base):
    __tablename__ = "schedules_new"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users_new.id"), nullable=False)
    course = Column(String(255), nullable=False)
    days = Column(JSON, nullable=False)  # ["Monday", "Wednesday", ...]
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)

    user = relationship("UsersNew", back_populates="schedules")
