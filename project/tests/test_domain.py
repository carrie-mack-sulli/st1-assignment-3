
"""Tests for SmartCare domain objects and validation rules."""

from datetime import datetime, timezone

import pytest

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)


def make_participants():
    """Create valid participants for appointment tests."""
    patient = Patient("P1", "Alex Example")
    practitioner = Practitioner("D1", "Taylor Example", "General")
    return patient, practitioner


# Patient tests
def test_blank_patient_id_is_rejected():
    with pytest.raises(ValueError):
        Patient(" ", "Alex Example")


def test_patient_stores_valid_fields():
    patient = Patient("P1", "Alex Example")

    assert patient.patient_id == "P1"
    assert patient.name == "Alex Example"


def test_blank_patient_name_is_rejected():
    with pytest.raises(ValueError):
        Patient("P1", " ")


# Practitioner tests
def test_practitioner_stores_valid_fields():
    practitioner = Practitioner("D1", "Taylor Example", "General")

    assert practitioner.practitioner_id == "D1"
    assert practitioner.name == "Taylor Example"
    assert practitioner.specialty == "General"


@pytest.mark.parametrize(
    ("practitioner_id", "name", "specialty"),
    [
        (" ", "Taylor Example", "General"),
        ("D1", " ", "General"),
        ("D1", "Taylor Example", " "),
    ],
)
def test_practitioner_rejects_blank_required_fields(
    practitioner_id, name, specialty
):
    with pytest.raises(ValueError):
        Practitioner(practitioner_id, name, specialty)


# Appointment construction tests
def test_appointment_starts_scheduled_and_stores_valid_fields():
    patient, practitioner = make_participants()
    appointment_time = datetime(2026, 10, 1, 9, 0)

    appointment = Appointment(
        "A1", patient, practitioner, appointment_time
    )

    assert appointment.appointment_id == "A1"
    assert appointment.patient is patient
    assert appointment.practitioner is practitioner
    assert appointment.date_time == appointment_time
    assert appointment.status is AppointmentStatus.SCHEDULED


def test_appointment_rejects_blank_id():
    patient, practitioner = make_participants()

    with pytest.raises(ValueError):
        Appointment(
            " ", patient, practitioner, datetime(2026, 10, 1, 9)
        )


@pytest.mark.parametrize(
    ("patient", "practitioner"),
    [
        (None, Practitioner("D1", "Taylor Example", "General")),
        (Patient("P1", "Alex Example"), None),
    ],
)
def test_appointment_rejects_invalid_participant_objects(
    patient, practitioner
):
    with pytest.raises(ValueError):
        Appointment(
            "A1", patient, practitioner, datetime(2026, 10, 1, 9)
        )


@pytest.mark.parametrize(
    "appointment_time",
    [
        "2026-10-01 09:00",
        datetime(2026, 10, 1, 9, 0, 1),
        datetime(2026, 10, 1, 9, 0, 0, 1),
        datetime(2026, 10, 1, 9, 0, tzinfo=timezone.utc),
    ],
)
def test_appointment_rejects_invalid_date_time(appointment_time):
    patient, practitioner = make_participants()

    with pytest.raises(ValueError):
        Appointment("A1", patient, practitioner, appointment_time)


def test_appointment_rejects_invalid_status():
    patient, practitioner = make_participants()

    with pytest.raises(ValueError):
        Appointment(
            "A1",
            patient,
            practitioner,
            datetime(2026, 10, 1, 9),
            "SCHEDULED",
        )


# Appointment cancellation tests
def test_cancel_changes_status():
    patient, practitioner = make_participants()
    appointment = Appointment(
        "A1", patient, practitioner, datetime(2026, 10, 1, 9)
    )

    appointment.cancel()

    assert appointment.status is AppointmentStatus.CANCELLED


def test_completed_appointment_cannot_be_cancelled():
    patient, practitioner = make_participants()
    appointment = Appointment(
        "A1",
        patient,
        practitioner,
        datetime(2026, 10, 1, 9),
        AppointmentStatus.COMPLETED,
    )

    with pytest.raises(ValueError):
        appointment.cancel()

    assert appointment.status is AppointmentStatus.COMPLETED
