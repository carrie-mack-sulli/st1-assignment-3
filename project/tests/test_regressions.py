"""Focused regression tests for the Stage 8 defects."""

from datetime import datetime

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def foundation():
    """Create a fresh store and register two patients and practitioners."""
    data_store = SmartCareDataStore()
    patient_service = PatientService(data_store)
    practitioner_service = PractitionerService(data_store)
    appointment_service = AppointmentService(data_store)

    patient1 = patient_service.register_patient("P1", "Alex Example")
    patient2 = patient_service.register_patient("P2", "Morgan Example")

    practitioner1 = practitioner_service.register_practitioner(
        "D1", "Taylor Example", "General"
    )
    practitioner2 = practitioner_service.register_practitioner(
        "D2", "Jordan Example", "Cardiology"
    )

    return (
        data_store,
        patient1,
        patient2,
        practitioner1,
        practitioner2,
        appointment_service,
    )


def test_f8_01_same_practitioner_conflict_and_different_practitioner_allowed():
    (
        data_store,
        patient1,
        patient2,
        practitioner1,
        practitioner2,
        appointment_service,
    ) = foundation()

    appointment_time = datetime(2026, 10, 1, 9, 0)

    original = appointment_service.book_appointment(
        "A1", patient1.patient_id, practitioner1.practitioner_id,
        appointment_time
    )

    # Attempt a second booking with the same practitioner and datetime.
    conflict_error = None

    try:
        appointment_service.book_appointment(
            "A2", patient2.patient_id, practitioner1.practitioner_id,
            appointment_time
        )
    except ValueError as error:
        conflict_error = error

    # The rejected booking must not change the stored appointments.
    assert isinstance(conflict_error, ValueError), (
        "A second scheduled appointment for the same practitioner "
        "and datetime should raise ValueError."
    )
    assert data_store.list_appointments() == [original]
    assert data_store.find_appointment("A2") is None

    # A different practitioner must be allowed at the same datetime.
    allowed = appointment_service.book_appointment(
        "A3", patient2.patient_id, practitioner2.practitioner_id,
        appointment_time
    )

    assert allowed.status is AppointmentStatus.SCHEDULED
    assert data_store.list_appointments() == [original, allowed]
    assert data_store.find_appointment("A3") is allowed


def test_f8_02_cancelled_appointment_remains_stored_and_retrievable():
    (
        data_store,
        patient1,
        _,
        practitioner1,
        _,
        appointment_service,
    ) = foundation()

    appointment_time = datetime(2026, 10, 1, 9, 0)

    appointment = appointment_service.book_appointment(
        "A1", patient1.patient_id, practitioner1.practitioner_id,
        appointment_time
    )

    cancelled = appointment_service.cancel_appointment("A1")

    # Cancellation should change the status, not remove the appointment.
    assert cancelled is appointment
    assert appointment.status is AppointmentStatus.CANCELLED

    # Check that the appointment remains in the store.
    assert appointment in data_store.list_appointments()
    assert data_store.find_appointment("A1") is appointment

    # The service should also retrieve the same stored object.
    assert appointment_service.find_appointment("A1") is appointment
