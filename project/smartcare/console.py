"""Console helpers and a small runnable starting demonstration."""


import re
from datetime import datetime

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def parse_date_time(text: str) -> datetime:
    """Parse YYYY-MM-DD HH:MM; raise ValueError for invalid input."""
    if (
        not isinstance(text, str)
        or re.fullmatch(
            '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}', text
        ) is None
    ):
        raise ValueError('Use date/time format YYYY-MM-DD HH:MM')
    try:
        return datetime.strptime(text, '%Y-%m-%d %H:%M')
    except ValueError:
        raise ValueError(
            'Invalid calendar date/time; use YYYY-MM-DD HH:MM',
        ) from None


def format_appointment(appointment: Appointment) -> str:
    """Return readable synthetic appointment details without changing
    state.
    """
    return (
        f'{appointment.appointment_id}: '
        f'{appointment.patient.patient_id} with '
        f'{appointment.practitioner.practitioner_id}, '
        f'{appointment.date_time:%Y-%m-%d %H:%M}, {appointment.status.value}'
    )


def run_demo() -> None:
    """Demonstrate supplied registration and booking using synthetic
    records.
    """
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)
    patients.register_patient('P1', 'Alex Example')
    practitioners.register_practitioner(
        'DR1',
        'Taylor Example',
        'General practice',
    )
    try:
        appointments.book_appointment(
            'A1',
            'P1',
            'DR1',
            parse_date_time('2026-10-01 09:00'),
        )
        print(format_appointment(appointments.find_appointment('A1')))
    except (ValueError, LookupError) as error:
        print(f'Error: {error}')
    print('Session-only data: records are lost on exit.')



def run_menu() -> None:
    """Run the interactive SmartCare session using in-memory records."""
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)

    while True:
        print("\n=== SmartCare Menu ===")
        print("1. Register patient")
        print("2. Find patient")
        print("3. Register practitioner")
        print("4. Find practitioner")
        print("5. Book appointment")
        print("6. Cancel appointment")
        print("7. Find appointment")
        print("8. List practitioner appointments")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Session ended. In-memory records are lost on exit.")
            break

        try:
            if choice == "1":
                patient_id = input("Patient ID: ")
                name = input("Patient name: ")
                patient = patients.register_patient(patient_id, name)
                print(f"Patient registered: {patient.patient_id}")

            elif choice == "2":
                patient_id = input("Patient ID: ")
                patient = patients.find_patient(patient_id)
                print(f"Patient found: {patient.patient_id}, {patient.name}")

            elif choice == "3":
                practitioner_id = input("Practitioner ID: ")
                name = input("Practitioner name: ")
                specialty = input("Specialty: ")
                practitioner = practitioners.register_practitioner(
                    practitioner_id, name, specialty
                )
                print(
                    f"Practitioner registered: "
                    f"{practitioner.practitioner_id}"
                )

            elif choice == "4":
                practitioner_id = input("Practitioner ID: ")
                practitioner = practitioners.find_practitioner(
                    practitioner_id
                )
                print(
                    f"Practitioner found: "
                    f"{practitioner.practitioner_id}, "
                    f"{practitioner.name}, {practitioner.specialty}"
                )

            elif choice == "5":
                appointment_id = input("Appointment ID: ")
                patient_id = input("Patient ID: ")
                practitioner_id = input("Practitioner ID: ")
                date_time = parse_date_time(
                    input("Date and time (YYYY-MM-DD HH:MM): ")
                )
                appointment = appointments.book_appointment(
                    appointment_id,
                    patient_id,
                    practitioner_id,
                    date_time,
                )
                print(f"Appointment booked: {format_appointment(appointment)}")

            elif choice == "6":
                appointment_id = input("Appointment ID: ")
                appointment = appointments.cancel_appointment(appointment_id)
                print(
                    f"Appointment cancelled: "
                    f"{format_appointment(appointment)}"
                )

            elif choice == "7":
                appointment_id = input("Appointment ID: ")
                appointment = appointments.find_appointment(appointment_id)
                print(f"Appointment found: {format_appointment(appointment)}")

            elif choice == "8":
                practitioner_id = input("Practitioner ID: ")
                status_text = input(
                    "Status (scheduled/cancelled/completed), "
                    "or press Enter for all: "
                ).strip().lower()

                if status_text == "":
                    status = None

                    try:
                        status = AppointmentStatus(status_text)
                    except ValueError:
                        raise ValueError(
                            "Status must be scheduled, cancelled or completed"
                        ) from None

                results = appointments.list_practitioner_appointments(
                    practitioner_id, status
                )

                if not results:
                    print("No matching appointments found.")
                else:
                    for appointment in results:
                        print(format_appointment(appointment))

            else:
                print("Unknown menu choice. Please choose a listed option.")

        except (ValueError, LookupError) as error:
            print(f"Error: {error}")

def run_menu() -> None:
    """Run the interactive SmartCare session using in-memory records."""
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)

    while True:
        print("\n=== SmartCare Menu ===")
        print("1. Register patient")
        print("2. Find patient")
        print("3. Register practitioner")
        print("4. Find practitioner")
        print("5. Book appointment")
        print("6. Cancel appointment")
        print("7. Find appointment")
        print("8. List practitioner appointments")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Session ended. In-memory records are lost on exit.")
            break

        try:
            if choice == "1":
                patient_id = input("Patient ID: ")
                name = input("Patient name: ")
                patient = patients.register_patient(patient_id, name)
                print(f"Patient registered: {patient.patient_id}")

            elif choice == "2":
                patient_id = input("Patient ID: ")
                patient = patients.find_patient(patient_id)
                print(f"Patient found: {patient.patient_id}, {patient.name}")

            elif choice == "3":
                practitioner_id = input("Practitioner ID: ")
                name = input("Practitioner name: ")
                specialty = input("Specialty: ")
                practitioner = practitioners.register_practitioner(
                    practitioner_id, name, specialty
                )
                print(
                    f"Practitioner registered: "
                    f"{practitioner.practitioner_id}"
                )

            elif choice == "4":
                practitioner_id = input("Practitioner ID: ")
                practitioner = practitioners.find_practitioner(
                    practitioner_id
                )
                print(
                    f"Practitioner found: "
                    f"{practitioner.practitioner_id}, "
                    f"{practitioner.name}, {practitioner.specialty}"
                )

            elif choice == "5":
                appointment_id = input("Appointment ID: ")
                patient_id = input("Patient ID: ")
                practitioner_id = input("Practitioner ID: ")
                date_time = parse_date_time(
                    input("Date and time (YYYY-MM-DD HH:MM): ")
                )
                appointment = appointments.book_appointment(
                    appointment_id,
                    patient_id,
                    practitioner_id,
                    date_time,
                )
                print(f"Appointment booked: {format_appointment(appointment)}")

            elif choice == "6":
                appointment_id = input("Appointment ID: ")
                appointment = appointments.cancel_appointment(appointment_id)
                print(
                    f"Appointment cancelled: "
                    f"{format_appointment(appointment)}"
                )

            elif choice == "7":
                appointment_id = input("Appointment ID: ")
                appointment = appointments.find_appointment(appointment_id)
                print(f"Appointment found: {format_appointment(appointment)}")

            elif choice == "8":
                practitioner_id = input("Practitioner ID: ")
                status_text = input(
                    "Status (scheduled/cancelled/completed), "
                    "or press Enter for all: "
                ).strip().lower()

                if status_text == "":
                    status = None
                else:
                    from smartcare.domain import AppointmentStatus

                    try:
                        status = AppointmentStatus(status_text)
                    except ValueError:
                        raise ValueError(
                            "Status must be scheduled, cancelled or completed"
                        ) from None

                results = appointments.list_practitioner_appointments(
                    practitioner_id, status
                )

                if not results:
                    print("No matching appointments found.")
                else:
                    for appointment in results:
                        print(format_appointment(appointment))

            else:
                print("Unknown menu choice. Please choose a listed option.")

        except (ValueError, LookupError) as error:
            print(f"Error: {error}")

