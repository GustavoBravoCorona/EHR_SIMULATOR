# Clinical Application Support & EHR Simulator

## Project Overview

I developed a **Clinical Application Support & EHR Simulator** to show how healthcare organizations can manage patient information, appointments, clinical encounters, and technical support requests through a centralized application.

I built this project using Python, Streamlit, SQLite, and Pandas to simulate common workflows found in healthcare information systems. The application includes interactive dashboards, patient record management, appointment scheduling, encounter documentation, support ticket tracking, and an audit log.

My goal was to strengthen my understanding of clinical application workflows, database management, data integrity, troubleshooting, and application support while building a project relevant to healthcare IT and Electronic Health Record (EHR) support roles.

## Technologies Used

- **Python** — Application logic and data processing.
- **Streamlit** — Interactive web application and user interface.
- **SQLite** — Database for storing and managing application records.
- **Pandas** — Data organization, display, and CSV export.

## Features

### 1. Dashboard
<img width="1510" height="857" alt="EHR_SIM_SC1" src="https://github.com/user-attachments/assets/e157abd4-7b0a-49ae-ad4c-fa362e6634f9" />

I developed a dashboard that provides an overview of the application's activity. It displays key metrics, including the number of patients, scheduled appointments, unresolved support tickets, and incomplete encounters. I also included ticket summaries and data-quality indicators to help identify issues that may require attention.

### 2. Patients
<img width="1512" height="891" alt="EHR_SIM_SC2" src="https://github.com/user-attachments/assets/b30f11dd-e903-4b9f-96fb-506d14ce574d" />

I created a patient management page where users can search and view fictional patient records. The page also allows users to add new patients. I implemented input validation and unique patient numbers to help maintain data consistency and reduce duplicate records.

### 3. Appointments
<img width="1512" height="891" alt="EHR_SIM_SC3" src="https://github.com/user-attachments/assets/6619dd7c-b964-4497-a689-486cc487e944" />

I built an appointment management page that allows users to review existing appointments and schedule new ones. Users can associate appointments with patient records and enter details such as appointment dates, visit types, and statuses. This feature simulates the scheduling workflows commonly used in healthcare environments.

### 4. Encounters
<img width="1512" height="891" alt="EHR_SIM_SC4" src="https://github.com/user-attachments/assets/8036a6db-a0c7-45df-b7f2-c1373397b3ee" />

I developed an encounter management page to simulate clinical documentation workflows. Users can create patient-associated encounters, select visit types, enter notes, and track whether required documentation is complete. I included completion indicators to make it easier to identify encounters that may need additional documentation.

### 5. Support Tickets
<img width="1512" height="891" alt="EHR_SIM_SC5" src="https://github.com/user-attachments/assets/692e8616-6391-4894-9813-493c9eaffd64" />

I implemented a support ticket management system to simulate clinical application support activities. Users can create tickets, categorize reported issues, assign priorities, update ticket statuses, and document resolutions. This feature shows how application support teams can organize requests, track troubleshooting progress, and monitor unresolved issues.

### 6. Users & Audit Log
<img width="1512" height="891" alt="EHR_SIM_SC6" src="https://github.com/user-attachments/assets/59b17839-3c88-44a5-8781-c9ad4b3ac528" />

I created a Users & Audit Log page to display user roles and provide visibility into recorded application activities. The audit log helps track supported actions, such as creating records and updating support tickets. I also included CSV export functionality so users can download audit information for review and analysis.

## Installation and Setup

Follow these steps to run the application locally.

### Prerequisites

- Python 3.9 or later
- pip (Python package installer)
- Git (optional, for cloning the repository)

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <your-project-folder>
```

Replace the placeholders with your actual GitHub repository URL and project folder name. Alternatively, download the project files and open the project directory in your terminal.

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

### 3. Activate the Virtual Environment

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
streamlit run app.py
```

Streamlit will provide a local URL, typically:

```text
http://localhost:8501
```

Open the URL in your web browser to interact with the application.

## Project Structure

```text
clinical-application-support-ehr-simulator/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

- `app.py` — Contains the Streamlit interface, application logic, database operations, and page functionality.
- `requirements.txt` — Lists the Python dependencies required to run the application.
- `README.md` — Documents the project, features, and setup instructions.
- `.gitignore` — Specifies files and directories that should not be committed to Git.

The SQLite database is created and populated with fictional records by the application as configured in the code.

## Skills Demonstrated

Through this project, I demonstrated experience with:

- Healthcare application and EHR workflow simulation
- Python application development
- Relational database management using SQLite
- Data validation and data integrity
- Patient record and appointment management
- Clinical encounter documentation workflows
- Support ticket creation, prioritization, and resolution tracking
- Application troubleshooting workflow design
- Audit logging and activity tracking
- Data reporting and CSV exports
- Interactive web application development
- Organizing and presenting information through dashboards

## Project Purpose

I created this project to connect my Computer Science background with healthcare IT and clinical application support. It allowed me to apply programming and database concepts to simulated healthcare workflows while exploring how technical support teams can help maintain accurate records, resolve application issues, and support clinical users.

This project is intended as a portfolio demonstration of my technical skills and interest in clinical applications, EHR systems, and healthcare technology support.

## Important Disclaimer

This is an educational demonstration project, **not a production Electronic Health Record system**. It uses fictional data and is not designed or validated for clinical use, regulatory compliance, or the storage of real patient information.

The application does not provide production-grade authentication, authorization, encryption, or comprehensive security controls. Do not enter real patient information or other sensitive data.

## Future Improvements

Potential future enhancements include:

- Implementing secure authentication and enforced role-based access controls
- Adding more detailed audit logging and searchable activity history
- Expanding support ticket reporting and analytics
- Improving input validation and error handling
- Adding automated tests for database operations and application workflows
- Integrating a more advanced database and secure deployment configuration
- Enhancing documentation and troubleshooting guidance for support staff

---

**Author:** Gustavo Bravo Corona  
**Project:** Clinical Application Support & EHR Simulator  
**Technologies:** Python, Streamlit, SQLite, Pandas
