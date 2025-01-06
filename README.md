# NMU Student Housing Management System

## Project Overview

The NMU Student Housing Management System is a web-based application designed to streamline the management of student housing facilities. It allows administrators to manage apartments, buildings, and maintenance requests, while students can apply for housing, view apartment details, and submit maintenance requests. The system also supports automated lease generation upon student signup.

---

## Features

### For Students:

- **Sign Up and Login**:
  - Secure signup and login using hashed passwords.
  - Automatic assignment of available apartments upon signup.
- **View Apartment Details**:
  - Access to apartment details such as floor and building location.
- **Maintenance Requests**:
  - Submit maintenance requests linked to assigned apartments.

### For Administrators:

- **Building Management**:
  - Manage buildings with attributes like location, capacity, and total floors.
- **Apartment Management**:
  - Assign apartments to specific buildings.
  - Update occupancy status.
- **Student Management**:
  - View, edit, and manage student details.
- **Maintenance Management**:
  - Track and resolve maintenance requests.

---

## Technologies Used

- **Backend**:
  - Flask (Python)
  - Flask-Login (User Authentication)
  - Flask-SQLAlchemy (Database ORM)
  - Flask-Admin (Admin Interface)
- **Frontend**:
  - HTML, CSS, Bootstrap, Javascript
- **Database**:
  - SQLite

---

## Setup and Installation

### Prerequisites

- Python 3.9 or later
- SQLite (pre-installed with Python)

### Installation Steps

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Lordiod/NMUstudenthousing.git
   cd NMUstudenthousing
   ```

2. **Activate The Virtual Environment**:

   ```bash
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Set Up the Database**:

   ```bash
   flask db upgrade
   ```

4. **Run the Application**:

   ```bash
   flask run
   ```

5. **Access the Application**:
   Open your web browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## API Endpoints

### Public Endpoints:

- `/signup`: Student signup page.
- `/login`: Student login page.

### Protected Endpoints:

- `/thankyou`: Confirmation page after successful signup.
- `/maintreq`: Maintenance request submission.

### Admin Endpoints:

- `/admin`: Admin dashboard for managing students, apartments, and buildings.

