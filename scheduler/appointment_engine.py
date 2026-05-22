from datetime import datetime
from scheduler.models import (
    Appointment, DoctorSchedule,
    AppointmentStatus, SessionLocal
)

def check_availability(doctor_name: str, date: str) -> list:
    db = SessionLocal()
    schedule = db.query(DoctorSchedule).filter_by(
        doctor_name=doctor_name, date=date
    ).first()

    if not schedule:
        db.close()
        return []

    all_slots = schedule.available_slots.split(",")
    booked = db.query(Appointment).filter_by(
        doctor_name=doctor_name,
        date=date,
        status=AppointmentStatus.booked
    ).all()

    booked_times = [a.time for a in booked]
    available = [s for s in all_slots if s not in booked_times]
    db.close()
    return available

def book_appointment(patient_id: str, doctor_name: str, date: str, time: str) -> dict:
    db = SessionLocal()
    try:
        slot_dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        if slot_dt < datetime.now():
            db.close()
            return {"success": False, "message": "Cannot book past appointments"}
    except:
        pass

    existing = db.query(Appointment).filter_by(
        doctor_name=doctor_name,
        date=date,
        time=time,
        status=AppointmentStatus.booked
    ).first()

    if existing:
        alternatives = check_availability(doctor_name, date)
        db.close()
        return {
            "success": False,
            "message": "Slot already booked",
            "alternatives": alternatives
        }

    appt = Appointment(
        patient_id=patient_id,
        doctor_id=f"doc_{doctor_name.replace(' ', '_').lower()}",
        doctor_name=doctor_name,
        date=date,
        time=time,
        status=AppointmentStatus.booked
    )
    db.add(appt)
    db.commit()
    db.close()
    return {
        "success": True,
        "message": f"Appointment booked with {doctor_name} on {date} at {time}"
    }

def cancel_appointment(patient_id: str, doctor_name: str, date: str) -> dict:
    db = SessionLocal()
    appt = db.query(Appointment).filter_by(
        patient_id=patient_id,
        doctor_name=doctor_name,
        date=date,
        status=AppointmentStatus.booked
    ).first()

    if not appt:
        db.close()
        return {"success": False, "message": "No appointment found to cancel"}

    appt.status = AppointmentStatus.cancelled
    db.commit()
    db.close()
    return {"success": True, "message": f"Appointment with {doctor_name} on {date} cancelled"}

def reschedule_appointment(
    patient_id: str, doctor_name: str,
    old_date: str, new_date: str, new_time: str
) -> dict:
    cancel_result = cancel_appointment(patient_id, doctor_name, old_date)
    if not cancel_result["success"]:
        return cancel_result
    return book_appointment(patient_id, doctor_name, new_date, new_time)