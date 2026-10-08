from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date

from app.database import get_db
from app.schemas import (
    StudentCreate,
    StudentUpdate,
    StudentPatch,
    StudentResponse,
    PaginatedStudentsResponse,
    MessageResponse
)
from app import crud

router = APIRouter(
    prefix="/students",
    tags=["Students CRUD"]
)


@router.post(
    "",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new student record",
    description="Add a new student profile to the SQLite database with unique student ID and email validation."
)
def create_student(
    student_in: StudentCreate,
    db: Session = Depends(get_db)
):
    # Check if student_id already exists
    existing_by_id = crud.get_student_by_custom_id(db, student_in.student_id.strip())
    if existing_by_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Student record with student_id '{student_in.student_id}' already exists."
        )

    # Check if email already exists
    existing_by_email = crud.get_student_by_email(db, student_in.email.strip())
    if existing_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Student record with email '{student_in.email}' already exists."
        )

    return crud.create_student(db, student_in)


@router.get(
    "",
    response_model=PaginatedStudentsResponse,
    status_code=status.HTTP_200_OK,
    summary="List and filter students",
    description="Retrieve a paginated list of students with optional search query, course filter, and date-of-birth range filtering."
)
def list_students(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=200, description="Max number of records to return"),
    search: Optional[str] = Query(None, description="Search keyword across name, student_id, email, or course"),
    course: Optional[str] = Query(None, description="Filter by course name"),
    born_after: Optional[date] = Query(None, description="Filter students born after this date (YYYY-MM-DD)"),
    born_before: Optional[date] = Query(None, description="Filter students born before this date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    items, total = crud.get_students(
        db,
        skip=skip,
        limit=limit,
        search=search,
        course=course,
        born_after=born_after,
        born_before=born_before
    )
    page = (skip // limit) + 1 if limit > 0 else 1
    return PaginatedStudentsResponse(
        total=total,
        page=page,
        page_size=len(items),
        items=items
    )


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve an individual student profile",
    description="Fetch a single student record by their primary ID or unique student_id (e.g., 'STU1001' or '1')."
)
def get_student(
    student_id: str,
    db: Session = Depends(get_db)
):
    student = crud.get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID '{student_id}' was not found in the database."
        )
    return student


@router.put(
    "/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    summary="Update all details of an existing student (Full Update)",
    description="Replace the details of an existing student profile."
)
def update_student(
    student_id: str,
    student_in: StudentUpdate,
    db: Session = Depends(get_db)
):
    db_student = crud.get_student_by_id(db, student_id)
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID '{student_id}' was not found in the database."
        )

    # If updating email, check collision with other students
    existing_by_email = crud.get_student_by_email(db, student_in.email)
    if existing_by_email and existing_by_email.id != db_student.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{student_in.email}' is already assigned to another student."
        )

    return crud.update_student(db, db_student, student_in)


@router.patch(
    "/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    summary="Modify specific fields of a student (Partial Update)",
    description="Update one or more attributes of an existing student profile without sending full entity."
)
def patch_student(
    student_id: str,
    student_in: StudentPatch,
    db: Session = Depends(get_db)
):
    db_student = crud.get_student_by_id(db, student_id)
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID '{student_id}' was not found in the database."
        )

    if student_in.email is not None:
        existing_by_email = crud.get_student_by_email(db, student_in.email)
        if existing_by_email and existing_by_email.id != db_student.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email '{student_in.email}' is already assigned to another student."
            )

    return crud.patch_student(db, db_student, student_in)


@router.delete(
    "/{student_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Remove a student record",
    description="Permanently delete a student record from the SQLite database."
)
def delete_student(
    student_id: str,
    db: Session = Depends(get_db)
):
    db_student = crud.get_student_by_id(db, student_id)
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID '{student_id}' was not found in the database."
        )

    deleted_student_id = db_student.student_id
    deleted_name = db_student.name
    crud.delete_student(db, db_student)

    return MessageResponse(
        message=f"Student record '{deleted_student_id}' ({deleted_name}) deleted successfully."
    )
