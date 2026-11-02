from datetime import datetime

import pytest

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)
from smartcare.queries import appointment_sort_key, select_appointments


@pytest.fixture
def appointment_data():
    patient = Patient("P1", "Test Patient")
    practitioner1 = Practitioner("D1", "Dr One", "General")
    practitioner2 = Practitioner("D2", "Dr Two", "Dental")

    appointments = [
        Appointment(
            "A3", patient, practitioner1,
            datetime(2026, 10, 1, 10, 0),
            AppointmentStatus.CANCELLED,
        ),
        Appointment(
            "A2", patient, practitioner1,
            datetime(2026, 10, 1, 9, 0),
            AppointmentStatus.SCHEDULED,
        ),
        Appointment(
            "A1", patient, practitioner1,
            datetime(2026, 10, 1, 9, 0),
            AppointmentStatus.COMPLETED,
        ),
        Appointment(
            "A4", patient, practitioner2,
            datetime(2026, 10, 1, 8, 0),
            AppointmentStatus.SCHEDULED,
        ),
    ]

    return appointments


def test_select_appointments_filters_by_practitioner(appointment_data):
    result = select_appointments(appointment_data, "D1")

    assert {a.practitioner.practitioner_id for a in result} == {"D1"}
    assert {a.appointment_id for a in result} == {"A1", "A2", "A3"}


@pytest.mark.parametrize(
    ("status", "expected_ids"),
    [
        (AppointmentStatus.SCHEDULED, {"A2", "A4"}),
        (AppointmentStatus.CANCELLED, {"A3"}),
        (AppointmentStatus.COMPLETED, {"A1"}),
        (None, {"A1", "A2", "A3", "A4"}),
    ],
)
def test_select_appointments_filters_by_status(
    appointment_data, status, expected_ids
):
    result = select_appointments(appointment_data, "D1", status)

    assert {a.appointment_id for a in result} == (
        expected_ids & {"A1", "A2", "A3"}
    )


def test_select_appointments_returns_empty_list_for_no_matches(appointment_data):
    result = select_appointments(appointment_data, "D99")

    assert result == []


def test_appointments_are_sorted_by_date_time_then_id(appointment_data):
    result = select_appointments(appointment_data, "D1")

    assert [a.appointment_id for a in result] == ["A1", "A2", "A3"]


def test_appointment_sort_key_returns_date_time_and_id(appointment_data):
    appointment = appointment_data[0]

    assert appointment_sort_key(appointment) == (
        datetime(2026, 10, 1, 10, 0),
        "A3",
    )


def test_query_returns_a_fresh_list_without_changing_source(appointment_data):
    original_order = appointment_data.copy()
    original_fields = [
        (a.appointment_id, a.date_time, a.status)
        for a in appointment_data
    ]

    result = select_appointments(appointment_data, "D1")

    assert result is not appointment_data
    assert appointment_data == original_order
    assert [
        (a.appointment_id, a.date_time, a.status)
        for a in appointment_data
    ] == original_fields


def test_repeated_calls_return_consistent_results(appointment_data):
    first_result = select_appointments(appointment_data, "D1")
    second_result = select_appointments(appointment_data, "D1")

    assert first_result == second_result
    assert first_result is not second_result


def test_empty_input_returns_a_fresh_list():
    result = select_appointments([], "D1")

    assert result == []
    assert result is not None


def test_already_sorted_input_is_not_mutated(appointment_data):
    appointments = sorted(appointment_data, key=appointment_sort_key)
    original_order = appointments.copy()

    result = select_appointments(appointments, "D1")

    assert appointments == original_order
    assert result is not appointments

def test_empty_input_returns_a_new_list():
    appointments = []

    result = select_appointments(appointments, "D1")

    assert result == []
    assert result is not appointments