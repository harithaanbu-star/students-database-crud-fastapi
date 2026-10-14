# 🎓 Students Database CRUD Application (+ Optional AI Extension)

**Python Backend Development Project** | **EWB Edu Tech Pvt. Ltd. Internship Assignment**

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/harithaanbu-star/students-database-crud-fastapi)

A high-performance, production-ready RESTful API built with **FastAPI** and **SQLite** for managing student records with full Create, Read, Update, and Delete (CRUD) operations, data validation, filtering, pagination, and an optional **Grounded Local AI query engine** powered by **Ollama**.

---

## 📌 Table of Contents
- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [Architecture & Directory Structure](#-architecture--directory-structure)
- [Technology Stack](#-technology-stack)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Running the Application](#-running-the-application)
- [Database Seeding](#-database-seeding)
- [Interactive API Documentation](#-interactive-api-documentation)
- [API Endpoints & Sample Requests](#-api-endpoints--sample-requests)
  - [1. Create Student](#1-create-student)
  - [2. List & Filter Students](#2-list--filter-students)
  - [3. Get Student by ID](#3-get-student-by-id)
  - [4. Update Student (Full Update - PUT)](#4-update-student-full-update---put)
  - [5. Update Student (Partial Update - PATCH)](#5-update-student-partial-update---patch)
  - [6. Delete Student](#6-delete-student)
  - [7. Bonus: Natural Language AI Query](#7-bonus-natural-language-ai-query)
- [Running Automated Tests](#-running-automated-tests)
- [Project Review Checklist](#-project-review-checklist)

---

## 🚀 Project Overview

This backend application satisfies all mandatory and optional requirements outlined in the EWB Internship Assignment:
1. **Full CRUD Operations**: Create, Read, Update, and Delete student records.
2. **Persistent Storage**: SQLite with SQLAlchemy ORM.
3. **Data Integrity & Validation**: Pydantic v2 schemas validating email formatting, unique student IDs, past date-of-birth constraints, and required fields.
4. **Search & Filtering**: Search across names, student IDs, emails, courses, and date-of-birth ranges with pagination support.
5. **Bonus Local AI Assistant**: Natural language querying over stored student records grounded in SQLite data without unrestricted SQL execution.

---

## ✨ Key Features

- **Standardized REST API**: Adheres to HTTP status codes (`201 Created`, `200 OK`, `400 Bad Request`, `404 Not Found`, `422 Unprocessable Entity`).
- **Flexible Lookups**: Query by either primary key integer ID (`/students/1`) or unique student ID (`/students/STU1001`).
- **Comprehensive Validation**:
  - Validates RFC-compliant email syntax.
  - Prevents duplicate Student IDs and duplicate Emails.
  - Ensures Date of Birth is strictly in the past.
- **Resilient AI Querying**:
  - Connects to local Ollama (`llama3.2:1b` or configurable).
  - Includes a safe, deterministic grounded context fallback if Ollama is offline or not installed.
- **Automated Testing Suite**: 100% test coverage for all endpoints and edge cases with pytest.

---

## 📂 Architecture & Directory Structure

```text
d:\Intern\
├── app\
│   ├── __init__.py            # Application package metadata
│   ├── config.py              # Application settings & environment variables
│   ├── database.py            # SQLite database engine, sessionmaker & Base
│   ├── models.py              # SQLAlchemy ORM Student model
│   ├── schemas.py             # Pydantic validation & response models
│   ├── crud.py                # Database queries and CRUD business logic
│   ├── ai_service.py          # Grounded AI query engine with Ollama integration
│   ├── main.py                # FastAPI app initialization, middleware & routes
│   └── routers\
│       ├── __init__.py        # Routers package
│       ├── students.py        # Student CRUD API routes
│       └── ai.py              # AI Natural Language query routes
├── tests\
│   ├── __init__.py            # Test package
│   ├── conftest.py            # Pytest fixtures & in-memory test database
│   ├── test_crud.py           # CRUD integration & validation test cases
│   └── test_ai.py             # AI endpoint tests
├── seed_data.py               # Database seeder with sample student data
├── requirements.txt           # Python project dependencies
├── .env.example               # Example environment variables
├── .gitignore                 # Standard Python gitignore
└── README.md                  # Complete project documentation
```

---

## 🛠️ Technology Stack

- **Language**: Python 3.10+ (tested on Python 3.14)
- **Web Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **ASGI Server**: [Uvicorn](https://www.uvicorn.org/)
- **ORM & Database**: [SQLAlchemy](https://www.sqlalchemy.org/) + [SQLite](https://www.sqlite.org/)
- **Data Validation**: [Pydantic v2](https://docs.pydantic.dev/)
- **Testing**: [Pytest](https://docs.pytest.org/)
- **HTTP Client**: [HTTPX](https://www.python-httpx.org/)
- **Local AI (Bonus)**: [Ollama](https://ollama.ai/) (e.g., `llama3.2:1b`)

---

## 📦 Prerequisites

- Python 3.10 or higher installed.
- (Optional for AI Bonus) [Ollama](https://ollama.com/) installed and running locally with `ollama run llama3.2:1b`.

---

## 🔧 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repository-url>
   cd Intern
   ```

2. **Create and activate a virtual environment** (recommended):
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables**:
   Copy `.env.example` to `.env` (optional, default values will be used if omitted):
   ```bash
   # Windows (PowerShell)
   Copy-Item .env.example .env

   # Linux / macOS
   cp .env.example .env
   ```

---

## 🚀 Running the Application

Start the FastAPI application using `uvicorn`:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Once running, access the application at:
- **API Base URL**: `http://localhost:8000`
- **Swagger UI Interactive Docs**: `http://localhost:8000/docs`
- **ReDoc Interactive Docs**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

---

## 🌾 Database Seeding

Populate the database with realistic sample student records:

```bash
python seed_data.py
```

Output:
```text
Initializing database tables...
Successfully seeded 6 sample student records into SQLite database.
```

---

## 📖 Interactive API Documentation

FastAPI provides built-in, interactive documentation with live execution:
- **Swagger UI**: Navigate to [http://localhost:8000/docs](http://localhost:8000/docs) to test all endpoints directly in your browser.
- **ReDoc**: Navigate to [http://localhost:8000/redoc](http://localhost:8000/redoc) for clean, readable API specifications.

---

## 📡 API Endpoints & Sample Requests

### 1. Create Student
- **Method**: `POST`
- **Endpoint**: `/students`
- **Status Code**: `201 Created`

#### Request Body:
```json
{
  "student_id": "STU1007",
  "name": "Vikram Seth",
  "date_of_birth": "2005-04-18",
  "email": "vikram.seth@example.com",
  "phone": "+91-9876501234",
  "course": "Computer Science",
  "address": "24 Lake View Road, Hyderabad, Telangana",
  "enrollment_date": "2024-07-01"
}
```

#### cURL:
```bash
curl -X POST "http://localhost:8000/students" \
     -H "Content-Type: application/json" \
     -d '{
       "student_id": "STU1007",
       "name": "Vikram Seth",
       "date_of_birth": "2005-04-18",
       "email": "vikram.seth@example.com",
       "phone": "+91-9876501234",
       "course": "Computer Science",
       "address": "24 Lake View Road, Hyderabad, Telangana",
       "enrollment_date": "2024-07-01"
     }'
```

---

### 2. List & Filter Students
- **Method**: `GET`
- **Endpoint**: `/students`
- **Query Parameters**:
  - `skip` (int, default=0)
  - `limit` (int, default=50)
  - `search` (string, optional keyword search across name, ID, email, or course)
  - `course` (string, optional filter by course)
  - `born_after` (YYYY-MM-DD, optional)
  - `born_before` (YYYY-MM-DD, optional)

#### cURL Examples:
```bash
# List all students
curl -X GET "http://localhost:8000/students"

# Filter by course
curl -X GET "http://localhost:8000/students?course=Data%20Science"

# Filter students born after 2005
curl -X GET "http://localhost:8000/students?born_after=2005-01-01"

# Search keyword
curl -X GET "http://localhost:8000/students?search=Aarav"
```

---

### 3. Get Student by ID
- **Method**: `GET`
- **Endpoint**: `/students/{student_id}` (Accepts primary key integer `1` or custom student ID `STU1001`)

#### cURL:
```bash
curl -X GET "http://localhost:8000/students/STU1001"
```

---

### 4. Update Student (Full Update - PUT)
- **Method**: `PUT`
- **Endpoint**: `/students/{student_id}`

#### Request Body:
```json
{
  "name": "Aarav Sharma",
  "date_of_birth": "2004-05-14",
  "email": "aarav.sharma.updated@example.com",
  "phone": "+91-9876543299",
  "course": "Artificial Intelligence & Data Science",
  "address": "99 Residency Road, Bengaluru, Karnataka",
  "enrollment_date": "2023-08-01"
}
```

#### cURL:
```bash
curl -X PUT "http://localhost:8000/students/STU1001" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Aarav Sharma",
       "date_of_birth": "2004-05-14",
       "email": "aarav.sharma.updated@example.com",
       "phone": "+91-9876543299",
       "course": "Artificial Intelligence & Data Science",
       "address": "99 Residency Road, Bengaluru, Karnataka",
       "enrollment_date": "2023-08-01"
     }'
```

---

### 5. Update Student (Partial Update - PATCH)
- **Method**: `PATCH`
- **Endpoint**: `/students/{student_id}`

#### Request Body (only fields to change):
```json
{
  "phone": "+91-9999911111",
  "course": "Full Stack Engineering"
}
```

#### cURL:
```bash
curl -X PATCH "http://localhost:8000/students/STU1001" \
     -H "Content-Type: application/json" \
     -d '{"phone": "+91-9999911111", "course": "Full Stack Engineering"}'
```

---

### 6. Delete Student
- **Method**: `DELETE`
- **Endpoint**: `/students/{student_id}`

#### cURL:
```bash
curl -X DELETE "http://localhost:8000/students/STU1007"
```

#### Response:
```json
{
  "message": "Student record 'STU1007' (Vikram Seth) deleted successfully."
}
```

---

### 7. Bonus: Natural Language AI Query
- **Method**: `POST`
- **Endpoint**: `/ai/query`

Ask questions in plain English grounded in current SQLite student records without unrestricted SQL execution.

#### Sample Questions:
1. `"How many students are there?"`
2. `"List students born after 2005."`
3. `"Show all students enrolled in Data Science."`

#### Request Body:
```json
{
  "question": "List students born after 2005."
}
```

#### cURL:
```bash
curl -X POST "http://localhost:8000/ai/query" \
     -H "Content-Type: application/json" \
     -d '{"question": "List students born after 2005."}'
```

#### Response:
```json
{
  "question": "List students born after 2005.",
  "answer": "Found 3 student(s) born after 2005:\n- Priya Patel (DOB: 2006-02-20, Course: Data Science)\n- Ananya Iyer (DOB: 2007-09-30, Course: Computer Science)\n- Sneha Mukherjee (DOB: 2006-12-03, Course: Data Science)",
  "records_analyzed": 6,
  "model_used": "Grounded Context Engine (Ollama Local Fallback)",
  "grounded_context_summary": "6 records grounded in SQLite database"
}
```

---

## 🧪 Running Automated Tests

A comprehensive test suite is included in `tests/` covering all CRUD operations, input validations, duplicate constraints, and AI query features.

Run the test suite with:

```bash
python -m pytest -v
```

Expected Output:
```text
============================= test session starts =============================
collected 13 items

tests/test_ai.py::test_ai_query_count_and_filters PASSED                 [  7%]
tests/test_crud.py::test_root_endpoint PASSED                            [ 15%]
tests/test_crud.py::test_health_check PASSED                             [ 23%]
tests/test_crud.py::test_create_student_success PASSED                   [ 30%]
tests/test_crud.py::test_create_student_duplicate_id PASSED              [ 38%]
tests/test_crud.py::test_create_student_duplicate_email PASSED           [ 46%]
tests/test_crud.py::test_create_student_validation_errors PASSED         [ 53%]
tests/test_crud.py::test_get_student_by_id_and_custom_id PASSED          [ 61%]
tests/test_crud.py::test_get_nonexistent_student PASSED                  [ 69%]
tests/test_crud.py::test_list_students_and_filtering PASSED              [ 76%]
tests/test_crud.py::test_update_student_put PASSED                       [ 84%]
tests/test_crud.py::test_patch_student PASSED                            [ 92%]
tests/test_crud.py::test_delete_student PASSED                           [100%]

======================== 13 passed in 5.41s ========================
```

---

## ✅ Project Review Checklist

- [x] **Create**: Add new student records with unique ID and email validation (`POST /students`).
- [x] **Read**: List all students with search & filtering (`GET /students`) and retrieve individual profiles (`GET /students/{id}`).
- [x] **Update**: Full update (`PUT /students/{id}`) and partial update (`PATCH /students/{id}`).
- [x] **Delete**: Remove student records from database (`DELETE /students/{id}`).
- [x] **Persistence**: SQLite database with SQLAlchemy ORM.
- [x] **Data Validation**: Strict Pydantic models preventing invalid emails, duplicate IDs/emails, and invalid dates of birth.
- [x] **Reproducible**: Self-contained seed script (`seed_data.py`), `requirements.txt`, and clear instructions.
- [x] **Bonus AI Feature**: Natural-language question answering grounded in database records via Ollama / fallback engine.
- [x] **Clean Repository**: `.gitignore` configured, no secrets or real personal data committed.

---

**Developed for**: Python Backend Development Internship | EWB Edu Tech Pvt. Ltd.
