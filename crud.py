from typing import List, Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext

import models
import schemas


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------- Password helpers ----------

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# ---------- Users ----------

def get_user_by_username(db: Session, username: str) -> Optional[models.UsersNew]:
    return db.query(models.UsersNew).filter(models.UsersNew.username == username).first()


def get_user(db: Session, user_id: int) -> Optional[models.UsersNew]:
    return db.query(models.UsersNew).filter(models.UsersNew.id == user_id).first()


def create_user_with_profile(db: Session, user: schemas.UserCreate) -> models.UsersNew:
    hashed = hash_password(user.password)
    db_user = models.UsersNew(username=user.username, password_hash=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    profile = models.UserProfilesNew(user_id=db_user.id)
    db.add(profile)
    db.commit()
    db.refresh(db_user)

    return db_user


# ---------- Profiles ----------

def get_user_profile(db: Session, user_id: int) -> Optional[models.UserProfilesNew]:
    return db.query(models.UserProfilesNew).filter(models.UserProfilesNew.user_id == user_id).first()


def update_user_profile(
    db: Session, user_id: int, profile_data: schemas.UserProfileUpdate
) -> models.UserProfilesNew:
    profile = get_user_profile(db, user_id)
    if profile is None:
        profile = models.UserProfilesNew(user_id=user_id)
        db.add(profile)
        db.commit()
        db.refresh(profile)

    data = profile_data.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)
    return profile


# ---------- Auth ----------

def authenticate_user(db: Session, username: str, password: str) -> Optional[models.UsersNew]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


# ---------- Schedules ----------

def create_schedule(db: Session, schedule: schemas.ScheduleCreate) -> models.SchedulesNew:
    db_schedule = models.SchedulesNew(
        user_id=schedule.user_id,
        course=schedule.course,
        days=schedule.days,
        start=schedule.start,
        end=schedule.end,
        building_id=schedule.building_id,
    )
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


def get_schedules_for_user(db: Session, user_id: int) -> List[models.SchedulesNew]:
    return db.query(models.SchedulesNew).filter(models.SchedulesNew.user_id == user_id).all()


def get_schedule(db: Session, schedule_id: int) -> Optional[models.SchedulesNew]:
    return db.query(models.SchedulesNew).filter(models.SchedulesNew.id == schedule_id).first()


def update_schedule(
    db: Session, schedule_id: int, schedule_data: schemas.ScheduleUpdate
) -> Optional[models.SchedulesNew]:
    schedule = get_schedule(db, schedule_id)
    if not schedule:
        return None

    data = schedule_data.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(schedule, key, value)

    db.commit()
    db.refresh(schedule)
    return schedule


def delete_schedule(db: Session, schedule_id: int) -> bool:
    schedule = get_schedule(db, schedule_id)
    if not schedule:
        return False
    db.delete(schedule)
    db.commit()
    return True
