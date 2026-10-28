"""Tests for the Stage 6 service operations."""

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def foundation():
    """Create a new store, registered participants and appointment service."""
    data_store = SmartCareDataStore()
    patient_service = PatientService(data_store)
    practitioner_service = PractitionerService(data_store)
    appointment_service = AppointmentService(data_store)

    patient = patient_service.register_patient("P1", "Alex Example")
    practitioner = practitioner_service.register_practitioner(
        "D1", "Taylor Example", "General"
    )

    return (
        data_store,
        patient,
        practitioner,
        patient_service,
        practitioner_service,
        appointment_service,
    )


def test_find_patient_returns_stored_object_and_accepts_trimmed_id():
    data_store, patient, _, patient_service, _, _ = foundation()

    assert patient_service.find_patient(" P1 ") is patient
    assert data_store.find_patient("P1") is patient


def test_find_patient_rejects_blank_and_unknown_ids():
    _, _, _, patient_service, _, _ = foundation()

    with pytest.raises(ValueError):
        patient_service.find_patient("  ")

    with pytest.raises(LookupError):
        patient_service.find_patient("missing")

    with pytest.raises(LookupError):
        patient_service.find_patient("p1")


def test_find_practitioner_returns_stored_object_and_accepts_trimmed_id():
    data_store, _, practitioner, _, practitioner_service, _ = foundation()

    assert practitioner_service.find_practitioner(" D1 ") is practitioner
    assert data_store.find_practitioner("D1") is practitioner


def test_find_practitioner_rejects_blank_and_unknown_ids():
    _, _, _, _, practitioner_service, _ = foundation()

    with pytest.raises(ValueError):
        practitioner_service.find_practitioner(" ")

    with pytest.raises(LookupError):
        practitioner_service.find_practitioner("missing")

    with pytest.raises(LookupError):
        practitioner_service.find_practitioner("d1")


def test_cancel_appointment_changes_status_and_retains_same_object():
    data_store, _, _, _, _, appointment_service = foundation()
    appointment = appointment_service.book_appointment(
        "A1", "P1", "D1", datetime(2026, 10, 1, 9)
    )

    cancelled = appointment_service.cancel_appointment(" A1 ")

    assert cancelled is appointment
    assert cancelled.status is AppointmentStatus.CANCELLED
    assert appointment_service.find_appointment("A1") is appointment
    assert data_store.list_appointments() == [appointment]


def test_cancel_appointment_rejects_unknown_and_blank_ids():
    _, _, _, _, _, appointment_service = foundation()

    with pytest.raises(ValueError):
        appointment_service.cancel_appointment(" ")

    with pytest.raises(LookupError):
        appointment_service.cancel_appointment("missing")


def test_repeated_cancellation_fails_without_changing_state():
    data_store, _, _, _, _, appointment_service = foundation()
    appointment = appointment_service.book_appointment(
        "A1", "P1", "D1", datetime(2026, 10, 1, 9)
    )
    appointment_service.cancel_appointment("A1")

    with pytest.raises(ValueError):
        appointment_service.cancel_appointment("A1")

    assert appointment.status is AppointmentStatus.CANCELLED
    assert data_store.find_appointment("A1") is appointment
    assert data_store.list_appointments() == [appointment]


def test_completed_appointment_cannot_be_cancelled():
    data_store, patient, practitioner, _, _, appointment_service = foundation()
    appointment = appointment_service.book_appointment(
        "A1", "P1", "D1", datetime(2026, 10, 1, 9)
    )

    # Build a completed appointment to test the domain's transition guard.
    completed = type(appointment)(
        "A2",
        patient,
        practitioner,
        datetime(2026, 10, 1, 10),
        AppointmentStatus.COMPLETED,
    )
    data_store.add_appointment(completed)

    with pytest.raises(ValueError):
        appointment_service.cancel_appointment("A2")

    assert completed.status is AppointmentStatus.COMPLETED
    assert appointment_service.find_appointment("A2") is completed
    assert data_store.list_appointments() == [appointment, completed]
