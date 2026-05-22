import json
from scheduler.appointment_engine import (
    check_availability,
    book_appointment,
    cancel_appointment,
    reschedule_appointment
)

def execute_tool(tool_name: str, args: dict) -> str:
    if tool_name == "check_availability":
        slots = check_availability(args["doctor_name"], args["date"])
        return f"Available slots: {', '.join(slots)}" if slots else "No slots available."

    elif tool_name == "book_appointment":
        result = book_appointment(
            args["patient_id"], args["doctor_name"],
            args["date"], args["time"]
        )
        return result["message"]

    elif tool_name == "cancel_appointment":
        result = cancel_appointment(
            args["patient_id"], args["doctor_name"], args["date"]
        )
        return result["message"]

    elif tool_name == "reschedule_appointment":
        result = reschedule_appointment(
            args["patient_id"], args["doctor_name"],
            args["old_date"], args["new_date"], args["new_time"]
        )
        return result["message"]

    return "Unknown tool called."