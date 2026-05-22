from scheduler.appointment_engine import (
    check_availability,
    book_appointment,
    cancel_appointment,
    reschedule_appointment
)
from memory.persistent_memory import (
    get_patient_profile,
    upsert_patient_profile
)


def handle_check_availability(doctor_name: str, date: str) -> dict:
    """
    Check available slots for a doctor on a given date.
    Returns list of available time slots.
    """
    slots = check_availability(doctor_name, date)

    if not slots:
        return {
            "success": False,
            "message": f"No available slots for {doctor_name} on {date}",
            "slots": []
        }

    return {
        "success": True,
        "message": f"Available slots for {doctor_name} on {date}",
        "slots": slots
    }


def handle_book_appointment(
    patient_id: str,
    doctor_name: str,
    date: str,
    time: str
) -> dict:
    """
    Book an appointment for a patient.
    Updates patient profile with last doctor visited.
    """
    result = book_appointment(patient_id, doctor_name, date, time)

    if result["success"]:
        # Update patient's last doctor in persistent memory
        upsert_patient_profile(patient_id, {
            "last_doctor": doctor_name
        })

    return result


def handle_cancel_appointment(
    patient_id: str,
    doctor_name: str,
    date: str
) -> dict:
    """
    Cancel an existing appointment.
    """
    result = cancel_appointment(patient_id, doctor_name, date)
    return result


def handle_reschedule_appointment(
    patient_id: str,
    doctor_name: str,
    old_date: str,
    new_date: str,
    new_time: str
) -> dict:
    """
    Reschedule an existing appointment to a new date and time.
    """
    result = reschedule_appointment(
        patient_id,
        doctor_name,
        old_date,
        new_date,
        new_time
    )
    return result


def handle_get_patient_info(patient_id: str) -> dict:
    """
    Get patient profile including preferences and history.
    """
    profile = get_patient_profile(patient_id)

    if not profile:
        return {
            "success": False,
            "message": "Patient profile not found"
        }

    return {
        "success": True,
        "profile": profile
    }


def handle_update_patient_language(
    patient_id: str,
    language: str
) -> dict:
    """
    Update patient's preferred language based on conversation.
    Called automatically when language is detected.
    """
    upsert_patient_profile(patient_id, {
        "preferred_language": language
    })

    return {
        "success": True,
        "message": f"Language preference updated to {language}"
    }