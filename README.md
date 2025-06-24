# NMU Student Housing Management System

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![Flask Version](https://img.shields.io/badge/flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A comprehensive web-based application designed to streamline Northern Michigan University's student housing operations. This system provides automated apartment assignment, maintenance request management, and administrative tools for efficient housing facility management.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Contributing](#contributing)
- [License](#license)

## Features

### Student Portal
- **Secure Authentication**
  - Password hashing with bcrypt
  - Session management with Flask-Login
  - Account registration and login
- **Automatic Housing Assignment**
  - Intelligent apartment allocation upon registration
  - Real-time availability checking
  - Preference-based assignment system
- **Apartment Information**
  - Detailed apartment specifications
  - Building and floor information
  - Roommate details and contact info
- **Maintenance Requests**
  - Easy-to-use request submission
  - Request status tracking
  - Photo upload capability
  - Priority level assignment

### Administrative Dashboard
- **Building Management**
  - Add, edit, and remove buildings
  - Capacity and floor management
  - Location and facility details
- **Apartment Management**
  - Apartment configuration and assignment
  - Occupancy status tracking
  - Maintenance history
- **Student Management**
  - Student profile management
  - Housing assignment oversight
  - Academic year tracking
- **Maintenance Management**
  - Request assignment to maintenance staff
  - Status updates and completion tracking
  - Resource allocation and scheduling
- **Reporting & Analytics**
  - Occupancy reports
  - Maintenance statistics
  - Financial summaries

## Tech Stack

### Backend
- **Framework**: Flask 2.0+
- **Authentication**: Flask-Login
- **Database ORM**: Flask-SQLAlchemy
- **Database Migrations**: Flask-Migrate
- **Admin Interface**: Flask-Admin
- **Password Hashing**: Werkzeug Security
- **Forms**: Flask-WTF

### Frontend
- **Templates**: Jinja2
- **Styling**: Bootstrap 5
- **JavaScript**: Vanilla JS
- **Icons**: Font Awesome

### Database
- **Development**: SQLite
- **Production**: PostgreSQL (recommended)

## Project Structure

```
NMUstudenthousing/
├── app/
│   ├── __init__.py
│   ├── models.py              # Database models
│   ├── routes.py              # Application routes
│   ├── forms.py               # WTF Forms
│   └── templates/
│       ├── base.html
│       ├── login.html
│       ├── signup.html
│       └── ...
├── migrations/                # Database migrations
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── venv/                      # Virtual environment
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
├── run.py                     # Application entry point
└── README.md
```

## Installation

### Prerequisites
- Python 3.9 or higher
- Git
- SQLite (included with Python)

### Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Lordiod/NMUstudenthousing.git
   cd NMUstudenthousing
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Edit .env with your configuration
   ```

5. **Initialize Database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Create Admin User** (Optional)
   ```bash
   flask create-admin
   ```

7. **Run the Application**
   ```bash
   flask run
   ```

8. **Access the Application**
   - Student Portal: [http://127.0.0.1:5000](http://127.0.0.1:5000)
   - Admin Dashboard: [http://127.0.0.1:5000/admin](http://127.0.0.1:5000/admin)

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///housing.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-email-password
```

### Database Configuration

For production, update `config.py`:

```python
class ProductionConfig(Config):
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'postgresql://user:pass@localhost/housing'
```

## Usage

### For Students

1. **Registration**: Visit `/signup` to create an account
2. **Login**: Access your portal at `/login`
3. **View Housing**: Check your assigned apartment details
4. **Submit Requests**: Use `/maintreq` for maintenance issues

### For Administrators

1. **Access Admin Panel**: Navigate to `/admin`
2. **Manage Buildings**: Add/edit building information
3. **Assign Apartments**: Manage student housing assignments
4. **Handle Requests**: Review and process maintenance requests

## API Documentation

### Authentication Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET    | `/signup` | Registration form | Public |
| POST   | `/signup` | Process registration | Public |
| GET    | `/login` | Login form | Public |
| POST   | `/login` | Process login | Public |
| GET    | `/logout` | User logout | Required |

### Student Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET    | `/dashboard` | Student dashboard | Required |
| GET    | `/apartment` | Apartment details | Required |
| GET    | `/maintreq` | Maintenance request form | Required |
| POST   | `/maintreq` | Submit maintenance request | Required |

### Admin Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET    | `/admin` | Admin dashboard | Admin |
| GET    | `/admin/students` | Manage students | Admin |
| GET    | `/admin/buildings` | Manage buildings | Admin |
| GET    | `/admin/apartments` | Manage apartments | Admin |

## Database Schema

### Core Models

#### Students Table
- **id_student** (int, Primary Key): Unique student identifier
- **studentid** (int): Student ID number
- **firstname** (varchar): Student's first name
- **secondname** (varchar): Student's last name
- **gender** (varchar): Student's gender
- **phone** (varchar): Contact phone number
- **faculty** (varchar): Academic faculty/department
- **year** (int): Year of study

#### Users Table
- **id** (int, Primary Key): Unique user identifier
- **username** (varchar): Login username
- **password** (varchar): Hashed password
- **is_admin** (boolean): Administrative privileges flag

#### Building Table
- **id_building** (int, Primary Key): Unique building identifier
- **building_num** (int): Building number
- **location** (varchar): Building location/address
- **capacity** (int): Total student capacity
- **total_floors** (int): Number of floors in building

#### Apartment Table
- **id_apt** (int, Primary Key): Unique apartment identifier
- **apt_num** (int): Apartment number
- **floor** (int): Floor number
- **fk_building** (int, Foreign Key): References building.id_building
- **lease_count** (int): Number of current leases

#### Lease Table
- **lease_id** (int, Primary Key): Unique lease identifier
- **fk_student** (int, Foreign Key): References students.id_student
- **fk_apartment** (int, Foreign Key): References apartment.id_apt
- **start_date** (date): Lease start date
- **end_date** (date): Lease end date
- **terms_and_conditions** (text): Lease terms and conditions
- **price** (decimal): Monthly rent amount

#### Maintenance_Request Table
- **request_id** (int, Primary Key): Unique request identifier
- **issue_description** (varchar): Description of the maintenance issue
- **date_reported** (datetime): When the request was submitted
- **status** (varchar): Current status (pending, in-progress, completed)
- **fk_apartment** (int, Foreign Key): References apartment.id_apt

### Entity Relationships

```
┌─────────────┐    1:N     ┌─────────────┐    N:1     ┌─────────────┐
│   Students  │◄──────────►│    Lease    │◄──────────►│  Apartment  │
└─────────────┘            └─────────────┘            └─────────────┘
                                                              │
                                                              │ N:1
                                                              ▼
                                                       ┌─────────────┐
                                                       │   Building  │
                                                       └─────────────┘
                                                              ▲
                                                              │ 1:N
┌─────────────┐    N:1                                       │
│Maintenance  │◄─────────────────────────────────────────────┘
│  Request    │            (via Apartment)
└─────────────┘
```

### Detailed Relationships

- **Students ↔ Lease**: One-to-Many (A student can have multiple leases over time)
- **Apartment ↔ Lease**: One-to-Many (An apartment can have multiple leases)
- **Building ↔ Apartment**: One-to-Many (A building contains multiple apartments)
- **Apartment ↔ Maintenance Request**: One-to-Many (An apartment can have multiple maintenance requests)

### Key Constraints

- Students must have unique student IDs
- Each lease links exactly one student to one apartment
- Apartments are uniquely identified within their building
- Maintenance requests are always associated with a specific apartment
- Buildings have capacity limits that should not be exceeded

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Star this repository if you find it helpful!**

