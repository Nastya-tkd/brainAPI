from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app import models, schemas, crud, auth, analysis
from app.database import SessionLocal, engine
from typing import List
from app.auth import router as auth_router
app.include_router(auth_router, prefix="/auth", tags=["auth"])

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login", response_model=schemas.Token)
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = auth.authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(auth.get_current_user)):
    return current_user

@app.post("/nanoparticles/", response_model=schemas.Nanoparticle)
def create_nanoparticle(
    nanoparticle: schemas.NanoparticleCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    return crud.create_nanoparticle(db=db, nanoparticle=nanoparticle)

@app.get("/nanoparticles/", response_model=List[schemas.Nanoparticle])
def read_nanoparticles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    nanoparticles = crud.get_nanoparticles(db, skip=skip, limit=limit)
    return nanoparticles

@app.get("/nanoparticles/{nanoparticle_id}", response_model=schemas.Nanoparticle)
def read_nanoparticle(nanoparticle_id: int, db: Session = Depends(get_db)):
    db_nanoparticle = crud.get_nanoparticle(db, nanoparticle_id=nanoparticle_id)
    if db_nanoparticle is None:
        raise HTTPException(status_code=404, detail="Nanoparticle not found")
    return db_nanoparticle

@app.put("/nanoparticles/{nanoparticle_id}", response_model=schemas.Nanoparticle)
def update_nanoparticle(
    nanoparticle_id: int,
    nanoparticle: schemas.NanoparticleCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    db_nanoparticle = crud.update_nanoparticle(db, nanoparticle_id=nanoparticle_id, nanoparticle=nanoparticle)
    if db_nanoparticle is None:
        raise HTTPException(status_code=404, detail="Nanoparticle not found")
    return db_nanoparticle

@app.delete("/nanoparticles/{nanoparticle_id}")
def delete_nanoparticle(
    nanoparticle_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    db_nanoparticle = crud.delete_nanoparticle(db, nanoparticle_id=nanoparticle_id)
    if db_nanoparticle is None:
        raise HTTPException(status_code=404, detail="Nanoparticle not found")
    return {"message": "Nanoparticle deleted successfully"}

@app.get("/analysis/compare", response_model=List[schemas.AnalysisResult])
def compare_nanoparticles(
    organ: str,
    nanoparticle_types: List[str],
    db: Session = Depends(get_db)
):
    return analysis.compare_nanoparticles(db, organ, nanoparticle_types)

@app.get("/analysis/most-effective", response_model=List[schemas.AnalysisResult])
def find_most_effective(
    target_organ: str,
    min_samples: int = 2,
    db: Session = Depends(get_db)
):
    return analysis.find_most_effective(db, target_organ, min_samples)