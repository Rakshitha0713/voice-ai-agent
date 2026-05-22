from scheduler.models import PatientProfile, SessionLocal

def get_patient_profile(patient_id: str) -> dict:
    db = SessionLocal()
    profile = db.query(PatientProfile).filter_by(patient_id=patient_id).first()
    db.close()
    if profile:
        return {
            "patient_id": profile.patient_id,
            "name": profile.name,
            "preferred_language": profile.preferred_language,
            "last_doctor": profile.last_doctor,
            "preferred_hospital": profile.preferred_hospital
        }
    return {}

def upsert_patient_profile(patient_id: str, updates: dict):
    db = SessionLocal()
    profile = db.query(PatientProfile).filter_by(patient_id=patient_id).first()
    if not profile:
        profile = PatientProfile(patient_id=patient_id, **updates)
        db.add(profile)
    else:
        for k, v in updates.items():
            setattr(profile, k, v)
    db.commit()
    db.close()