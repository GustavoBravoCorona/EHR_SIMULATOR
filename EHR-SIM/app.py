
import sqlite3
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import streamlit as st

# --------------------------------------------------
# Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Clinical Application Support Simulator",
    page_icon="",
    layout="wide",
)

DB_PATH = Path(__file__).parent / "clinical_demo.db"

ROLES = {
    "Administrator": [
        "Dashboard", "Patients", "Appointments",
        "Encounters", "Support Tickets", "Users & Audit Log"
    ],
    "Clinical Staff": [
        "Dashboard", "Patients", "Appointments",
        "Encounters", "Support Tickets"
    ],
    "Application Support": [
        "Dashboard", "Patients", "Appointments",
        "Encounters", "Support Tickets", "Users & Audit Log"
    ],
}


# --------------------------------------------------
# Database
# --------------------------------------------------

def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with connect() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_number TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            phone TEXT DEFAULT '',
            email TEXT DEFAULT '',
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            appointment_date TEXT NOT NULL,
            appointment_type TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Scheduled',
            notes TEXT DEFAULT '',
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        );

        CREATE TABLE IF NOT EXISTS encounters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            encounter_date TEXT NOT NULL,
            visit_type TEXT NOT NULL,
            note TEXT NOT NULL,
            required_field_complete INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        );

        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Open',
            description TEXT NOT NULL,
            assignee TEXT DEFAULT '',
            resolution TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS app_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            display_name TEXT NOT NULL,
            role TEXT NOT NULL,
            active INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            actor_role TEXT NOT NULL,
            action TEXT NOT NULL,
            entity_type TEXT NOT NULL,
            entity_id TEXT NOT NULL,
            details TEXT DEFAULT '',
            created_at TEXT NOT NULL
        );
        """)

        # Seed the database only once.
        if conn.execute("SELECT COUNT(*) FROM patients").fetchone()[0] == 0:
            now = datetime.now().isoformat(timespec="seconds")

            conn.executemany("""
                INSERT INTO patients
                (patient_number, first_name, last_name,
                 date_of_birth, phone, email, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, [
                ("DEMO-1001", "Jordan", "Lee", "1988-04-12",
                 "555-0101", "jordan.lee@example.test", now),
                ("DEMO-1002", "Morgan", "Rivera", "1994-09-23",
                 "555-0102", "morgan.rivera@example.test", now),
                ("DEMO-1003", "Taylor", "Patel", "1976-01-07",
                 "555-0103", "taylor.patel@example.test", now),
            ])

            conn.executemany("""
                INSERT INTO appointments
                (patient_id, appointment_date, appointment_type,
                 status, notes)
                VALUES (?, ?, ?, ?, ?)
            """, [
                (1, date.today().isoformat(), "Primary care follow-up",
                 "Scheduled", "Demo appointment"),
                (2, date.today().isoformat(), "Preventive visit",
                 "Checked in", "Demo appointment"),
                (3, date.today().isoformat(), "Lab review",
                 "Completed", " Demo appointment"),
            ])

            conn.executemany("""
                INSERT INTO encounters
                (patient_id, encounter_date, visit_type, note,
                 required_field_complete, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, [
                (1, date.today().isoformat(), "Follow-up",
                 "Synthetic training note.", 1, now),
                (2, date.today().isoformat(), "Preventive visit",
                 "Synthetic note; review required fields.", 0, now),
            ])

            conn.executemany("""
                INSERT INTO tickets
                (title, category, priority, status, description,
                 assignee, resolution, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                ("Encounter form missing required field",
                 "Clinical documentation", "High", "Open",
                 "A required field is not being validated before save.",
                 "Application Support", "", now, now),
                ("Unable to find appointment",
                 "Scheduling", "Medium", "In Progress",
                 "User cannot locate a scheduled appointment.",
                 "Application Support", "", now, now),
                ("Request for report export",
                 "Reporting", "Low", "Resolved",
                 "Staff member needs instructions for exporting a report.",
                 "Application Support", "Export steps documented.",
                 now, now),
            ])

            conn.executemany("""
                INSERT INTO app_users (display_name, role)
                VALUES (?, ?)
            """, [
                ("Demo Administrator", "Administrator"),
                ("Demo Clinical Staff", "Clinical Staff"),
                ("Demo Support Analyst", "Application Support"),
            ])


def read_df(sql, params=()):
    with connect() as conn:
        return pd.read_sql_query(sql, conn, params=params)


def log_action(role, action, entity, entity_id, details=""):
    with connect() as conn:
        conn.execute("""
            INSERT INTO audit_log
            (actor_role, action, entity_type, entity_id,
             details, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            role, action, entity, str(entity_id), details,
            datetime.now().isoformat(timespec="seconds")
        ))


def patient_options():
    df = read_df("""
        SELECT id, patient_number, first_name, last_name
        FROM patients ORDER BY last_name, first_name
    """)
    labels = {
        int(row.id):
        f"{row.patient_number} — {row.first_name} {row.last_name}"
        for row in df.itertuples()
    }
    return labels


init_db()


# --------------------------------------------------
# Sidebar and page navigation
# --------------------------------------------------

st.title("Clinical Application Support & EHR Simulator")


with st.sidebar:
    st.header("Workspace")
    role = st.selectbox("Role", list(ROLES.keys()))
    page = st.radio("Navigation", ROLES[role])
    st.divider()
    


# --------------------------------------------------
# Dashboard
# --------------------------------------------------

if page == "Dashboard":
    st.header("Application overview")

    patients = read_df("SELECT COUNT(*) AS n FROM patients").iloc[0]["n"]
    appointments = read_df(
        "SELECT COUNT(*) AS n FROM appointments"
    ).iloc[0]["n"]
    open_tickets = read_df("""
        SELECT COUNT(*) AS n FROM tickets
        WHERE status != 'Resolved'
    """).iloc[0]["n"]
    incomplete = read_df("""
        SELECT COUNT(*) AS n FROM encounters
        WHERE required_field_complete = 0
    """).iloc[0]["n"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Patients", int(patients))
    c2.metric("Appointments", int(appointments))
    c3.metric("Unresolved tickets", int(open_tickets))
    c4.metric("Incomplete encounters", int(incomplete))

    st.subheader("Support tickets")
    st.dataframe(read_df("""
        SELECT id, title, category, priority, status,
               assignee, updated_at
        FROM tickets
        ORDER BY CASE priority
            WHEN 'Critical' THEN 1
            WHEN 'High' THEN 2
            WHEN 'Medium' THEN 3
            ELSE 4 END,
            updated_at DESC
    """), use_container_width=True, hide_index=True)

    st.subheader("Documentation quality")
    flagged = read_df("""
        SELECT e.id AS encounter_id, p.patient_number,
               e.encounter_date, e.visit_type
        FROM encounters e
        JOIN patients p ON p.id = e.patient_id
        WHERE e.required_field_complete = 0
    """)

    if flagged.empty:
        st.success("No incomplete encounters found.")
    else:
        st.warning(f"{len(flagged)} encounter(s) need review.")
        st.dataframe(flagged, use_container_width=True, hide_index=True)


# --------------------------------------------------
# Patient directory
# --------------------------------------------------

elif page == "Patients":
    st.header("Patient directory")

    search = st.text_input("Search by name or patient number")
    patients = read_df("""
        SELECT patient_number, first_name, last_name,
               date_of_birth, phone, email
        FROM patients
        WHERE patient_number LIKE ?
           OR first_name LIKE ?
           OR last_name LIKE ?
        ORDER BY last_name, first_name
    """, (f"%{search}%", f"%{search}%", f"%{search}%"))

    st.dataframe(patients, use_container_width=True, hide_index=True)

    st.subheader("Add a fictional patient")
    with st.form("add_patient"):
        col1, col2 = st.columns(2)
        first = col1.text_input("First name *")
        last = col2.text_input("Last name *")
        dob = col1.date_input(
            "Date of birth",
            value=date(1990, 1, 1),
            min_value=date(1900, 1, 1),
            max_value=date.today()
        )
        number = col2.text_input("Patient number *",
                                 placeholder="DEMO-1004")
        phone = col1.text_input("Phone (optional)", "555-0104")
        email = col2.text_input(
            "Email (optional)", "person@example.test"
        )

        submitted = st.form_submit_button("Add patient")

        if submitted:
            if not first.strip() or not last.strip() or not number.strip():
                st.error("First name, last name, and patient number are required.")
            elif not number.strip().startswith("DEMO-"):
                st.error("Use a patient number beginning with DEMO-.")
            elif email.strip() and not email.strip().lower().endswith(
                ("@example.test", "@example.com", "@example.org")
            ):
                st.error("Use a reserved example email domain for data.")
            else:
                try:
                    with connect() as conn:
                        cur = conn.execute("""
                            INSERT INTO patients
                            (patient_number, first_name, last_name,
                             date_of_birth, phone, email, created_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (
                            number.strip(), first.strip(), last.strip(),
                            dob.isoformat(), phone.strip(), email.strip(),
                            datetime.now().isoformat(timespec="seconds")
                        ))
                        new_id = cur.lastrowid

                    log_action(role, "CREATE", "patient", new_id,
                               f"Created {number.strip()}")
                    st.success("Fictional patient added.")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("That patient number already exists.")


# --------------------------------------------------
# Appointments
# --------------------------------------------------

elif page == "Appointments":
    st.header("Appointment scheduling")

    appointments = read_df("""
        SELECT a.id, p.patient_number,
               p.first_name || ' ' || p.last_name AS patient,
               a.appointment_date, a.appointment_type,
               a.status, a.notes
        FROM appointments a
        JOIN patients p ON p.id = a.patient_id
        ORDER BY a.appointment_date DESC
    """)
    st.dataframe(appointments, use_container_width=True, hide_index=True)

    labels = patient_options()
    st.subheader("Schedule an appointment")

    if labels:
        with st.form("add_appointment"):
            patient_id = st.selectbox(
                "Patient", list(labels),
                format_func=lambda x: labels[x]
            )
            appt_date = st.date_input("Appointment date", date.today())
            appt_type = st.selectbox("Appointment type", [
                "Primary care follow-up", "Preventive visit",
                "Lab review", "Dental visit", "Other"
            ])
            status = st.selectbox("Status", [
                "Scheduled", "Checked in", "Completed", "Cancelled"
            ])
            notes = st.text_area("Administrative notes (no sensitive details)")

            if st.form_submit_button("Save appointment"):
                with connect() as conn:
                    cur = conn.execute("""
                        INSERT INTO appointments
                        (patient_id, appointment_date, appointment_type,
                         status, notes)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        patient_id, appt_date.isoformat(),
                        appt_type, status, notes.strip()
                    ))
                    appointment_id = cur.lastrowid

                log_action(role, "CREATE", "appointment", appointment_id,
                           appt_type)
                st.success("Appointment saved.")
                st.rerun()
    else:
        st.info("Add a patient before scheduling an appointment.")


# --------------------------------------------------
# Encounter documentation
# --------------------------------------------------

elif page == "Encounters":
    st.header("Clinical documentation simulator")

    encounters = read_df("""
        SELECT e.id, p.patient_number,
               p.first_name || ' ' || p.last_name AS patient,
               e.encounter_date, e.visit_type,
               CASE WHEN e.required_field_complete = 1
                    THEN 'Complete' ELSE 'Needs review' END AS documentation_status,
               e.note
        FROM encounters e
        JOIN patients p ON p.id = e.patient_id
        ORDER BY e.encounter_date DESC
    """)
    st.dataframe(encounters, use_container_width=True, hide_index=True)

    labels = patient_options()
    st.subheader("Add a simulated encounter")

    if labels:
        with st.form("add_encounter"):
            patient_id = st.selectbox(
                "Patient", list(labels),
                format_func=lambda x: labels[x]
            )
            encounter_date = st.date_input("Encounter date", date.today())
            visit_type = st.selectbox("Visit type", [
                "Follow-up", "Preventive visit",
                "Dental visit", "Lab review", "Other"
            ])
            note = st.text_area(
                "Synthetic training note",
                placeholder="Example: Note for workflow testing."
            )
            complete = st.checkbox(
                "Required documentation fields reviewed and complete"
            )

            if st.form_submit_button("Save encounter"):
                if not note.strip():
                    st.error("Enter a synthetic training note.")
                else:
                    with connect() as conn:
                        cur = conn.execute("""
                            INSERT INTO encounters
                            (patient_id, encounter_date, visit_type, note,
                             required_field_complete, created_at)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (
                            patient_id, encounter_date.isoformat(),
                            visit_type, note.strip(), int(complete),
                            datetime.now().isoformat(timespec="seconds")
                        ))
                        encounter_id = cur.lastrowid

                    log_action(role, "CREATE", "encounter", encounter_id,
                               f"Documentation complete={complete}")
                    st.success("Simulated encounter saved.")
                    st.rerun()
    else:
        st.info("Add a patient before creating an encounter.")


# --------------------------------------------------
# Support ticket management
# --------------------------------------------------

elif page == "Support Tickets":
    st.header("Clinical application support tickets")

    tickets = read_df("""
        SELECT id, title, category, priority, status,
               assignee, description, resolution, created_at, updated_at
        FROM tickets
        ORDER BY updated_at DESC
    """)
    st.dataframe(tickets, use_container_width=True, hide_index=True)

    st.subheader("Create a ticket")
    with st.form("new_ticket"):
        title = st.text_input("Issue title *")
        category = st.selectbox("Category", [
            "Access/Login", "Clinical documentation", "Scheduling",
            "Reporting", "Data quality", "Interface/integration", "Other"
        ])
        priority = st.selectbox(
            "Priority", ["Low", "Medium", "High", "Critical"]
        )
        description = st.text_area(
            "Issue description *",
            placeholder="Describe the system behavior. Do not include patient identifiers."
        )
        assignee = st.text_input("Assigned to", "Application Support")

        submitted = st.form_submit_button("Create ticket")

        if submitted:
            if not title.strip() or not description.strip():
                st.error("Title and description are required.")
            else:
                now = datetime.now().isoformat(timespec="seconds")
                with connect() as conn:
                    cur = conn.execute("""
                        INSERT INTO tickets
                        (title, category, priority, status, description,
                         assignee, created_at, updated_at)
                        VALUES (?, ?, ?, 'Open', ?, ?, ?, ?)
                    """, (
                        title.strip(), category, priority,
                        description.strip(), assignee.strip(), now, now
                    ))
                    ticket_id = cur.lastrowid

                log_action(role, "CREATE", "ticket", ticket_id, title.strip())
                st.success(f"Ticket #{ticket_id} created.")
                st.rerun()

    st.subheader("Update an existing ticket")
    ticket_list = read_df("SELECT id, title, status FROM tickets ORDER BY id DESC")

    if not ticket_list.empty:
        ids = ticket_list["id"].tolist()
        selected_id = st.selectbox(
            "Select ticket",
            ids,
            format_func=lambda x: (
                f"#{x} — "
                f"{ticket_list.loc[ticket_list.id == x, 'title'].iloc[0]}"
            )
        )

        current = read_df(
            "SELECT * FROM tickets WHERE id = ?", (selected_id,)
        ).iloc[0]

        with st.form("update_ticket"):
            statuses = ["Open", "In Progress", "Waiting on User", "Resolved"]
            priorities = ["Low", "Medium", "High", "Critical"]

            new_status = st.selectbox(
                "Status", statuses, index=statuses.index(current["status"])
            )
            new_priority = st.selectbox(
                "Priority", priorities,
                index=priorities.index(current["priority"])
            )
            new_assignee = st.text_input(
                "Assignee", value=current["assignee"] or ""
            )
            resolution = st.text_area(
                "Troubleshooting and resolution notes",
                value=current["resolution"] or ""
            )

            if st.form_submit_button("Update ticket"):
                now = datetime.now().isoformat(timespec="seconds")
                with connect() as conn:
                    conn.execute("""
                        UPDATE tickets
                        SET status = ?, priority = ?, assignee = ?,
                            resolution = ?, updated_at = ?
                        WHERE id = ?
                    """, (
                        new_status, new_priority, new_assignee.strip(),
                        resolution.strip(), now, int(selected_id)
                    ))

                log_action(role, "UPDATE", "ticket", selected_id,
                           f"Status={new_status}; Priority={new_priority}")
                st.success("Ticket updated.")
                st.rerun()


# --------------------------------------------------
# Users and audit log
# --------------------------------------------------

elif page == "Users & Audit Log":
    st.header("Users and audit log")
  

    st.subheader("Users")
    users = read_df("""
        SELECT id, display_name, role,
               CASE WHEN active = 1 THEN 'Active' ELSE 'Inactive' END AS status
        FROM app_users ORDER BY id
    """)
    st.dataframe(users, use_container_width=True, hide_index=True)

    st.subheader("Audit log")
    audit = read_df("""
        SELECT created_at, actor_role, action,
               entity_type, entity_id, details
        FROM audit_log ORDER BY id DESC LIMIT 200
    """)

    if audit.empty:
        st.info("No actions logged yet. Create a record or update a ticket.")
    else:
        st.dataframe(audit, use_container_width=True, hide_index=True)
        st.download_button(
            "Download audit log CSV",
            data=audit.to_csv(index=False).encode("utf-8"),
            file_name="demo_audit_log.csv",
            mime="text/csv"
        )


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

