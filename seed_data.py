"""
Database Seeder Script
Populates the SQLite database with realistic sample student records.
"""

from datetime import date
from app.database import SessionLocal, Base, engine
from app.models import Student

SAMPLE_STUDENTS = [
    {
        "student_id": "STU1001",
        "name": "Aarav Sharma",
        "date_of_birth": date(2004, 5, 14),
        "email": "aarav.sharma@example.com",
        "phone": "+91-9876543210",
        "course": "Computer Science",
        "address": "42 MG Road, Bengaluru, Karnataka",
        "enrollment_date": date(2023, 8, 1)
    },
    {
        "student_id": "STU1002",
        "name": "Priya Patel",
        "date_of_birth": date(2006, 2, 20),
        "email": "priya.patel@example.com",
        "phone": "+91-9811223344",
        "course": "Data Science",
        "address": "15 Park Street, Ahmedabad, Gujarat",
        "enrollment_date": date(2024, 1, 15)
    },
    {
        "student_id": "STU1003",
        "name": "Rohan Verma",
        "date_of_birth": date(2003, 11, 8),
        "email": "rohan.verma@example.com",
        "phone": "+91-9988776655",
        "course": "Cybersecurity",
        "address": "88 Civil Lines, Delhi",
        "enrollment_date": date(2022, 7, 20)
    },
    {
        "student_id": "STU1004",
        "name": "Ananya Iyer",
        "date_of_birth": date(2007, 9, 30),
        "email": "ananya.iyer@example.com",
        "phone": "+91-9765432190",
        "course": "Computer Science",
        "address": "12 TTK Road, Chennai, Tamil Nadu",
        "enrollment_date": date(2024, 8, 10)
    },
    {
        "student_id": "STU1005",
        "name": "Karan Malhotra",
        "date_of_birth": date(2005, 7, 12),
        "email": "karan.malhotra@example.com",
        "phone": "+91-9823456781",
        "course": "Machine Learning",
        "address": "5B Linking Road, Mumbai, Maharashtra",
        "enrollment_date": date(2023, 8, 5)
    },
    {
        "student_id": "STU1006",
        "name": "Sneha Mukherjee",
        "date_of_birth": date(2006, 12, 3),
        "email": "sneha.m@example.com",
        "phone": "+91-9830123456",
        "course": "Data Science",
        "address": "77 Salt Lake, Kolkata, West Bengal",
        "enrollment_date": date(2024, 2, 1)
    }
]


def seed_database():
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        added_count = 0
        for item in SAMPLE_STUDENTS:
            existing = db.query(Student).filter(Student.student_id == item["student_id"]).first()
            if not existing:
                student = Student(**item)
                db.add(student)
                added_count += 1
        db.commit()
        print(f"Successfully seeded {added_count} sample student records into SQLite database.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
