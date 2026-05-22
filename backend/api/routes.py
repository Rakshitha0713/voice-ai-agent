from fastapi import APIRouter
from pydantic import BaseModel
from backend.controllers.appointment_controller import (
    handle_check_availability,
    handle_book_appointment,
    handle_cancel_appointment,
    handle_reschedule_appointment,
    handle_get_patient_info
)

router = APIRouter(prefix="/api")


class BookRequest(BaseModel):
    patient_id: str
    doctor_name: str
    date: str
    time: str


class CancelRequest(BaseModel):
    patient_id: str
    doctor_name: str
    date: str


class RescheduleRequest(BaseModel):
    patient_id: str
    doctor_name: str
    old_date: str
    new_date: str
    new_time: str


@router.get("/availability")
def get_availability(doctor_name: str, date: str):
    return handle_check_availability(doctor_name, date)


@router.post("/book")
def book(req: BookRequest):
    return handle_book_appointment(
        req.patient_id,
        req.doctor_name,
        req.date,
        req.time
    )


@router.post("/cancel")
def cancel(req: CancelRequest):
    return handle_cancel_appointment(
        req.patient_id,
        req.doctor_name,
        req.date
    )


@router.post("/reschedule")
def reschedule(req: RescheduleRequest):
    return handle_reschedule_appointment(
        req.patient_id,
        req.doctor_name,
        req.old_date,
        req.new_date,
        req.new_time
    )


@router.get("/patient/{patient_id}")
def get_patient(patient_id: str):
    return handle_get_patient_info(patient_id)