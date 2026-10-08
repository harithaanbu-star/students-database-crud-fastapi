from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import List, Optional, Tuple
from datetime import date

from app.models import Student
from app.schemas import StudentCreate, StudentUpdate, StudentPatch


def get_student_by_id(db: Session, student_id_or_pk: str) -> Optional[Student]:
    """
    Find student by primary key ID (if integer) or by student_id string (e.g. STU1001).
    """
    if student_id_or_pk.isdigit():
        student = db.query(Student).filter(Student.id == int(student_id_or_pk)).first()
        if student:
            return student
    return db.query(Student).filter(Student.student_id == student_id_or_pk).first()


def get_student_by_custom_id(db: Session, student_id: str) -> Optional[Student]:
    return db.query(Student).filter(Student.student_id == student_id).first()


def get_student_by_email(db: Session, email: str) -> Optional[Student]:
    return db.query(Student).filter(func.lower(Student.email) == email.lower()).first()


def get_students(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    search: Optional[str] = None,
    course: Optional[str] = None,
    born_after: Optional[date] = None,
    born_before: Optional[date] = None
) -> Tuple[List[Student], int]:
    """
    Retrieve students with optional filtering and pagination.
    Returns (list_of_students, total_count).
    """
    query = db.query(Student)

    if search:
        search_pattern = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Student.name.ilike(search_pattern),
                Student.student_id.ilike(search_pattern),
                Student.email.ilike(search_pattern),
                Student.course.ilike(search_pattern)
            )
        )

    if course:
        query = query.filter(Student.course.ilike(f"%{course.strip()}%"))

    if born_after:
        query = query.filter(Student.date_of_birth > born_after)

    if born_before:
        query = query.filter(Student.date_of_birth < born_before)

    total = query.count()
    items = query.order_by(Student.id.desc()).offset(skip).limit(limit).all()
    return items, total


def create_student(db: Session, student_in: StudentCreate) -> Student:
    db_student = Student(
        student_id=student_in.student_id.strip(),
        name=student_in.name.strip(),
        date_of_birth=student_in.date_of_birth,
        email=student_in.email.strip().lower(),
        phone=student_in.phone.strip() if student_in.phone else None,
        course=student_in.course.strip() if student_in.course else None,
        address=student_in.address.strip() if student_in.address else None,
        enrollment_date=student_in.enrollment_date,
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def update_student(db: Session, db_student: Student, student_in: StudentUpdate) -> Student:
    db_student.name = student_in.name.strip()
    db_student.date_of_birth = student_in.date_of_birth
    db_student.email = student_in.email.strip().lower()
    db_student.phone = student_in.phone.strip() if student_in.phone else None
    db_student.course = student_in.course.strip() if student_in.course else None
    db_student.address = student_in.address.strip() if student_in.address else None
    if student_in.enrollment_date is not None:
        db_student.enrollment_date = student_in.enrollment_date

    db.commit()
    db.refresh(db_student)
    return db_student


def patch_student(db: Session, db_student: Student, student_in: StudentPatch) -> Student:
    update_data = student_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if isinstance(value, str):
            value = value.strip()
        if field == "email" and value:
            value = value.lower()
        setattr(db_student, field, value)

    db.commit()
    db.refresh(db_student)
    return db_student


def delete_student(db: Session, db_student: Student) -> None:
    db.delete(db_student)
    db.commit()


def get_all_students_for_ai(db: Session, limit: int = 150) -> List[Student]:
    return db.query(Student).order_by(Student.id.asc()).limit(limit).all()
