from sqlalchemy.orm import Session
from app import models, schemas

def get_nanoparticle(db: Session, nanoparticle_id: int):
    return db.query(models.Nanoparticle).filter(models.Nanoparticle.id == nanoparticle_id).first()

def get_nanoparticles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Nanoparticle).offset(skip).limit(limit).all()

def create_nanoparticle(db: Session, nanoparticle: schemas.NanoparticleCreate):
    db_nanoparticle = models.Nanoparticle(**nanoparticle.model_dump())
    db.add(db_nanoparticle)
    db.commit()
    db.refresh(db_nanoparticle)
    return db_nanoparticle

def update_nanoparticle(db: Session, nanoparticle_id: int, nanoparticle: schemas.NanoparticleCreate):
    db_nanoparticle = db.query(models.Nanoparticle).filter(models.Nanoparticle.id == nanoparticle_id).first()
    if db_nanoparticle:
        for key, value in nanoparticle.model_dump().items():
            setattr(db_nanoparticle, key, value)
        db.commit()
        db.refresh(db_nanoparticle)
    return db_nanoparticle

def delete_nanoparticle(db: Session, nanoparticle_id: int):
    db_nanoparticle = db.query(models.Nanoparticle).filter(models.Nanoparticle.id == nanoparticle_id).first()
    if db_nanoparticle:
        db.delete(db_nanoparticle)
        db.commit()
    return db_nanoparticle

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    from .auth import get_password_hash
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user