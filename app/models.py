from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Nanoparticle(Base):
    __tablename__ = 'nanoparticles'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    accumulations = relationship("AccumulationData", back_populates="nanoparticle")


class Experiment(Base):
    __tablename__ = 'experiments'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    accumulations = relationship("AccumulationData", back_populates="experiment")


class AccumulationData(Base):
    __tablename__ = 'accumulation_data'
    id = Column(Integer, primary_key=True)
    nanoparticle_id = Column(Integer, ForeignKey('nanoparticles.id'))
    experiment_id = Column(Integer, ForeignKey('experiments.id'))
    mouse_number = Column(Integer)
    lungs = Column(Float)
    liver = Column(Float)
    kidneys = Column(Float)
    spleen = Column(Float)
    brain = Column(Float)
    heart = Column(Float)

    nanoparticle = relationship("Nanoparticle", back_populates="accumulations")
    experiment = relationship("Experiment", back_populates="accumulations")