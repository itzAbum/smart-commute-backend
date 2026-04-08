from typing import List, Optional
from datetime import time

from pydantic import BaseModel, EmailStr


# ---------- User ----------

class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True


# ---------- Profile ----------

class UserProfileBase(BaseModel):
    email: Optional[EmailStr] = None
    home_address: Optional[str] = None


class UserProfileUpdate(UserProfileBase):
    pass


class UserProfileOut(UserProfileBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


# ---------- Schedule ----------

class ScheduleBase(BaseModel):
    course: str
    days: List[str]
    start: time
    end: time


class ScheduleCreate(ScheduleBase):
    user_id: int


class ScheduleUpdate(BaseModel):
    course: Optional[str] = None
    days: Optional[List[str]] = None
    start: Optional[time] = None
    end: Optional[time] = None


class ScheduleOut(ScheduleBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


# ---------- Auth ----------

class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    user_id: int
