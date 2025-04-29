from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    username: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class NanoparticleBase(BaseModel):
    nanoparticle_type: str
    experiment_condition: str
    mouse_number: int
    lungs: float
    liver: float
    kidneys: float
    spleen: float
    brain: float
    heart: float

class NanoparticleCreate(NanoparticleBase):
    pass

class Nanoparticle(NanoparticleBase):
    id: int

    class Config:
        from_attributes = True

class AnalysisResult(BaseModel):
    nanoparticle_type: str
    organ: str
    average_accumulation: float