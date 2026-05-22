import os
import enum
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import Column, Integer, String, Enum, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv('DATABASE_URL')
Base = declarative_base()

class DoctorSchedule(Base):
    __tablename__ = 'doctor_schedule'
    id = Column(Integer, primary_key=True)
    doctor_id = Column(String)
    doctor_name = Column(String)
    specialization = Column(String)
    date = Column(String)
    available_slots = Column(Integer)

class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True)
    patient_id = Column(String)
    doctor_id = Column(String)
    date = Column(String)
    time = Column(String)

class PatientProfile(Base):
    __tablename__ = 'patient_profiles'
    id = Column(Integer, primary_key=True)
    patient_id = Column(String, unique=True)
    name = Column(String)
    preferred_language = Column(String)
    last_doctor = Column(String)
    preferred_hospital = Column(String)

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
print("Tables created successfully!")