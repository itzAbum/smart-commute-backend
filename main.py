from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
import schemas
import crud
from database import engine, Base, get_db

# Create tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI()

print(">>> RUNNING UPDATED MAIN.PY WITH NEW CORS <<<")

# ---------------- CORS FIX ----------------
# These are the ONLY origins your frontend uses.
# "*" does NOT work when allow_credentials=True.
# Browsers block the request unless the exact origin is listed.
origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -------------------------------------------

#Edit 123
# ---------- Auth ----------

@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_username(db, user.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )
    new_user = crud.create_user_with_profile(db, user)
    return new_user


@app.post("/login", response_model=schemas.LoginResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, payload.username, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return schemas.LoginResponse(user_id=user.id)


# ---------- Users & Profiles ----------

@app.get("/users/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users/{user_id}/profile", response_model=schemas.UserProfileOut)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    profile = crud.get_user_profile(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@app.put("/users/{user_id}/profile", response_model=schemas.UserProfileOut)
def update_profile(
    user_id: int, profile_data: schemas.UserProfileUpdate, db: Session = Depends(get_db)
):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    profile = crud.update_user_profile(db, user_id, profile_data)
    return profile


# ---------- Schedules ----------

@app.post("/schedules/", response_model=schemas.ScheduleOut)
def create_schedule(schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    user = crud.get_user(db, schedule.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_schedule = crud.create_schedule(db, schedule)
    return db_schedule


@app.get("/schedules/{user_id}", response_model=list[schemas.ScheduleOut])
def get_schedules(user_id: int, db: Session = Depends(get_db)):
    return crud.get_schedules_for_user(db, user_id)


@app.put("/schedules/{schedule_id}", response_model=schemas.ScheduleOut)
def update_schedule(
    schedule_id: int, schedule_data: schemas.ScheduleUpdate, db: Session = Depends(get_db)
):
    updated = crud.update_schedule(db, schedule_id, schedule_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return updated


@app.delete("/schedules/{schedule_id}")
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_schedule(db, schedule_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return {"detail": "Schedule deleted"}


# ---------- Recommendation placeholder ----------

@app.get("/recommendation/{user_id}")
def get_recommendation(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user_id": user_id,
        "recommendation": "Feature coming soon – plug your logic here."
    }
