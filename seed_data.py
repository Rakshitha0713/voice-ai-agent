import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from scheduler.models import SessionLocal, DoctorSchedule, PatientProfile

db = SessionLocal()

try:
    doctors = [
        DoctorSchedule(
            doctor_id="doc_001",
            doctor_name="Dr. Sharma",
            specialization="Cardiologist",
            date="2026-06-01",
            available_slots="09:00,10:00,11:00,14:00,15:00"
        ),
        DoctorSchedule(
            doctor_id="doc_002",
            doctor_name="Dr. Priya",
            specialization="Dermatologist",
            date="2026-06-01",
            available_slots="09:30,10:30,13:00,14:30"
        ),
        DoctorSchedule(
            doctor_id="doc_003",
            doctor_name="Dr. Kumar",
            specialization="General Physician",
            date="2026-06-01",
            available_slots="08:00,09:00,10:00,11:00"
        ),
    ]

    patient = PatientProfile(
        patient_id="patient_001",
        name="Test Patient",
        preferred_language="english",
        last_doctor="Dr. Sharma",
        preferred_hospital="Apollo"
    )

    for doc in doctors:
        db.add(doc)
    db.add(patient)
    db.commit()
    print("Seed data added successfully!")

except Exception as e:
    print(f"Error: {e}")
    db.rollback()
finally:
    db.close()