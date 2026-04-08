from sqlalchemy import Column, Integer, String, ForeignKey, Time
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship

from database import Base



class UsersNew(Base):
    __tablename__ = "users_new"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    profile = relationship("UserProfilesNew", back_populates="user", uselist=False)
    schedules = relationship("SchedulesNew", back_populates="user")


class UserProfilesNew(Base):
    __tablename__ = "user_profiles_new"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users_new.id"), nullable=False)
    email = Column(String(255), nullable=True)
    home_address = Column(String(255), nullable=True)

    user = relationship("UsersNew", back_populates="profile")


class SchedulesNew(Base):
    __tablename__ = "schedules_new"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users_new.id"), nullable=False)
    course = Column(String(255), nullable=False)
    days = Column(JSON, nullable=False)  # ["Monday", "Wednesday", ...]
    start = Column(Time, nullable=False)
    end = Column(Time, nullable=False)

    user = relationship("UsersNew", back_populates="schedules")
