import re
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
from datetime import date, datetime

EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'


def validate_email_address(v: str) -> str:
    v = v.strip().lower()
    if not re.match(EMAIL_REGEX, v):
        raise ValueError("Invalid email address format.")
    return v


class StudentBase(BaseModel):
    student_id: str = Field(..., min_length=1, max_length=50, description="Unique identifier for the student (e.g. STU1001)")
    name: str = Field(..., min_length=1, max_length=100, description="Full name of the student")
    date_of_birth: date = Field(..., description="Date of birth in YYYY-MM-DD format")
    email: str = Field(..., max_length=150, description="Valid contact email address")
    phone: Optional[str] = Field(None, max_length=30, description="Contact phone number")
    course: Optional[str] = Field(None, max_length=100, description="Enrolled course name")
    address: Optional[str] = Field(None, max_length=255, description="Residential address")
    enrollment_date: Optional[date] = Field(default_factory=date.today, description="Date of enrollment")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty or whitespace.")
        return v

    @field_validator("student_id")
    @classmethod
    def validate_student_id(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Student ID cannot be empty.")
        return v

    @field_validator("email")
    @classmethod
    def check_email(cls, v: str) -> str:
        return validate_email_address(v)

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob(cls, v: date) -> date:
        if v >= date.today():
            raise ValueError("Date of birth must be in the past.")
        return v


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    """Schema for full update (PUT)"""
    name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date = Field(...)
    email: str = Field(..., max_length=150)
    phone: Optional[str] = Field(None, max_length=30)
    course: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=255)
    enrollment_date: Optional[date] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty or whitespace.")
        return v

    @field_validator("email")
    @classmethod
    def check_email(cls, v: str) -> str:
        return validate_email_address(v)

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob(cls, v: date) -> date:
        if v >= date.today():
            raise ValueError("Date of birth must be in the past.")
        return v


class StudentPatch(BaseModel):
    """Schema for partial update (PATCH)"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    date_of_birth: Optional[date] = None
    email: Optional[str] = Field(None, max_length=150)
    phone: Optional[str] = Field(None, max_length=30)
    course: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=255)
    enrollment_date: Optional[date] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Name cannot be empty or whitespace.")
        return v

    @field_validator("email")
    @classmethod
    def check_email(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return validate_email_address(v)
        return v

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob(cls, v: Optional[date]) -> Optional[date]:
        if v is not None and v >= date.today():
            raise ValueError("Date of birth must be in the past.")
        return v


class StudentResponse(StudentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaginatedStudentsResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[StudentResponse]


class MessageResponse(BaseModel):
    message: str
    detail: Optional[str] = None


class AIQueryRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=500, description="Natural language question about student records")


class AIQueryResponse(BaseModel):
    question: str
    answer: str
    records_analyzed: int
    model_used: str
    grounded_context_summary: Optional[str] = None
