
from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def create_workflow():
    data_store = SmartCareDataStore()
    patient_service = PatientService(data_store)
    practitioner_service = PractitionerService(data_store)
    appointment_service = AppointmentService(data_store)

    patient_service.register_patient("P1", "Test Patient")
    practitioner_service.register_practitioner(
        "D1", "Dr One", "General Practice"
    )
    practitioner_service.register_practitioner(
        "D2", "Dr Two", "General Practice"
    )

    return data_store, appointment_service


def test_workflow_books_cancels_and_retains_appointment_history():
    data_store, service = create_workflow()

    appointment = service.book_appointment(
        "A1", "P1", "D1", datetime(2026, 10, 1, 9, 0)
    )

    cancelled = service.cancel_appointment("A1")

    assert cancelled is appointment
    assert appointment.status == AppointmentStatus.CANCELLED
    assert service.find_appointment("A1") is appointment
    assert service.list_practitioner_appointments("D1") == [appointment]
    assert data_store.find_appointment("A1") is appointment


def test_cancelled_appointment_is_excluded_from_scheduled_listing():
    _, service = create_workflow()

    service.book_appointment(
        "A1", "P1", "D1", datetime(2026, 10, 1, 9, 0)
    )
    service.cancel_appointment("A1")

    assert service.list_practitioner_appointments(
        "D1", AppointmentStatus.SCHEDULED
    ) == []


def test_cancelled_slot_can_be_booked_again_for_same_practitioner():
    _, service = create_workflow()

    original = service.book_appointment(
        "A1", "P1", "D1", datetime(2026, 10, 1, 9, 0)
    )
    service.cancel_appointment("A1")

    replacement = service.book_appointment(
        "A2", "P1", "D1", datetime(2026, 10, 1, 9, 0)
    )

    assert original.status == AppointmentStatus.CANCELLED
    assert replacement.status == AppointmentStatus.SCHEDULED
    assert service.find_appointment("A1") is original
    assert service.find_appointment("A2") is replacement


def test_same_practitioner_and_time_conflict_is_rejected_without_changes():
    data_store, service = create_workflow()

    original = service.book_appointment(
        "A1", "P1", "D1", datetime(2026, 10, 1, 9, 0)
    )
    before = data_store.list_appointments()

    with pytest.raises(ValueError):
        service.book_appointment(
            "A2", "P1", "D1", datetime(2026, 10, 1, 9, 0)
        )

    after = data_store.list_appointments()

    assert after == before
    assert after[0] is original
    with pytest.raises(LookupError):
        service.find_appointment("A2")


def test_different_practitioners_can_have_appointments_at_same_time():
    _, service = create_workflow()
    appointment_time = datetime(2026, 10, 1, 9, 0)

    first = service.book_appointment("A1", "P1", "D1", appointment_time)
    second = service.book_appointment("A2", "P1", "D2", appointment_time)

    assert first.practitioner.practitioner_id == "D1"
    assert second.practitioner.practitioner_id == "D2"


def test_unknown_patient_booking_is_rejected_without_changing_appointments():
    data_store, service = create_workflow()
    before = data_store.list_appointments()

    with pytest.raises(LookupError):
        service.book_appointment(
            "A1", "UNKNOWN", "D1", datetime(2026, 10, 1, 9, 0)
        )

    assert data_store.list_appointments() == before
    with pytest.raises(LookupError):
        service.find_appointment("A1")
