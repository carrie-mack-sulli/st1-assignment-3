# SmartCare Application
Requirements baseline: SmartCare A3 2026 revision 2. Python 3.13 and pytest 8.3.5 verified. Runtime uses only the Python standard library.

## Working directory and commands
Run all application and test commands from this project/ directory, using the approved Python environment with the development dependency installed.

Run the demonstration:

python main.py

Start the interactive console menu:

python main.py --interactive

Run the cumulative test suite:

python -m pytest -q

If needed, install the development dependency in the approved environment:

python -m pip install -r requirements-dev.txt

## Application functionality
The SmartCare application supports:

Registering and finding patients.

Registering and finding practitioners.

Booking appointments.

Cancelling appointments.

Finding appointments and retrieving appointment history.

Listing appointments for a practitioner, with an optional status filter.

The interactive menu repeats until the user chooses to exit. Expected validation and lookup errors are reported so the user can correct input and continue.

## Data and limitations
Synthetic data only is used. Patient, practitioner and appointment records are held in memory during the application session. Data is not persisted and is lost when the application exits. FR-10 restart persistence is retired.

No PG rescheduling or assurance solution is included in the common Stage 9 application.

## Application structure
domain.py contains the domain entities, appointment status and guarded cancellation.

data_store.py stores patients, practitioners and appointments in dictionaries and provides add, find and list methods.

services.py coordinates operations using the shared data store.

queries.py contains the pure appointment query and sorting functions.

console.py handles interactive input, output, menu navigation and expected errors.

The services share the same data-store object during a menu session. Lists returned by store and query operations are new containers holding the relevant stored appointment objects.

## Validation and behaviour
IDs are trimmed, non-blank and case-sensitive. Service booking accepts IDs and a datetime (local, minute precision). The console date parser accepts exactly YYYY-MM-DD HH:MM.

Store lookups return None when an item is absent; service lookups raise LookupError. Invalid values, duplicates, conflicts and illegal state transitions raise ValueError.

Appointment cancellation changes the appointment status; it does not delete the appointment record. Cancelled appointments remain available in appointment history and can be included in unfiltered practitioner appointment listings.

No age, duration, patient-conflict or past-date rules apply.

## Stage 9 verification
The test command was python -m pytest -q, run from the project/ directory. Manual interactive checks covered the normal booking and cancellation workflow and recovery from invalid input.

Further implementation and verification details are recorded in the Stage 9 activities and evidence record.