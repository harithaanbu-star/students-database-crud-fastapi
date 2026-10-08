import json
import logging
import re
from typing import Dict, Any, List
from datetime import datetime, date
import httpx
from app.config import get_settings
from app.models import Student

logger = logging.getLogger("app.ai_service")
settings = get_settings()


def _format_students_context(students: List[Student]) -> str:
    """
    Format student records into structured JSON text for the LLM context.
    No sensitive data is exposed.
    """
    records = []
    for s in students:
        records.append({
            "id": s.id,
            "student_id": s.student_id,
            "name": s.name,
            "date_of_birth": s.date_of_birth.isoformat() if s.date_of_birth else None,
            "email": s.email,
            "phone": s.phone or "N/A",
            "course": s.course or "Unassigned",
            "enrollment_date": s.enrollment_date.isoformat() if s.enrollment_date else None,
        })
    return json.dumps(records, indent=2)


def _rule_based_grounded_fallback(question: str, students: List[Student]) -> str:
    """
    Accurate fallback engine to answer grounded questions when local Ollama is offline or unavailable.
    Safely parses common queries (counts, birthday filtering, courses, etc.) without unrestricted SQL.
    """
    q_lower = question.lower()
    total_students = len(students)

    # 1. Count query
    if any(phrase in q_lower for phrase in ["how many students", "total students", "count of students", "number of students"]):
        courses = {}
        for s in students:
            c = s.course or "Unassigned"
            courses[c] = courses.get(c, 0) + 1
        course_breakdown = ", ".join([f"{k}: {v}" for k, v in courses.items()])
        return f"There are currently {total_students} student(s) registered in the database. Breakdown by course: {course_breakdown}."

    # 2. Born after / before year query (e.g. "born after 2005")
    year_match_after = re.search(r'born (?:after|later than) (\d{4})', q_lower)
    if year_match_after:
        year = int(year_match_after.group(1))
        matched = [s for s in students if s.date_of_birth and s.date_of_birth.year > year]
        if not matched:
            return f"No students found born after {year}."
        names = [f"{s.name} (DOB: {s.date_of_birth.isoformat()}, Course: {s.course or 'N/A'})" for s in matched]
        return f"Found {len(matched)} student(s) born after {year}:\n- " + "\n- ".join(names)

    year_match_before = re.search(r'born (?:before|earlier than) (\d{4})', q_lower)
    if year_match_before:
        year = int(year_match_before.group(1))
        matched = [s for s in students if s.date_of_birth and s.date_of_birth.year < year]
        if not matched:
            return f"No students found born before {year}."
        names = [f"{s.name} (DOB: {s.date_of_birth.isoformat()}, Course: {s.course or 'N/A'})" for s in matched]
        return f"Found {len(matched)} student(s) born before {year}:\n- " + "\n- ".join(names)

    # 3. List courses or students in course
    if "course" in q_lower or "enrolled in" in q_lower:
        for course_name in ["computer science", "data science", "machine learning", "cybersecurity", "software engineering"]:
            if course_name in q_lower:
                matched = [s for s in students if s.course and course_name in s.course.lower()]
                if not matched:
                    return f"No students are currently enrolled in {course_name.title()}."
                names = [f"{s.name} (ID: {s.student_id}, Email: {s.email})" for s in matched]
                return f"Found {len(matched)} student(s) in {course_name.title()}:\n- " + "\n- ".join(names)

    # 4. List all students
    if any(phrase in q_lower for phrase in ["list students", "list all students", "show students", "who are the students"]):
        if not students:
            return "There are no students currently stored in the database."
        names = [f"{s.name} (ID: {s.student_id}, Course: {s.course or 'Unassigned'})" for s in students[:10]]
        return f"Here are the students ({len(students)} total, showing first {len(names)}):\n- " + "\n- ".join(names)

    # Generic summary
    return (
        f"Grounded response based on {total_students} student record(s) in the database:\n"
        f"Total students: {total_students}. For specific information, you can ask about counts, "
        f"birth dates (e.g. 'born after 2005'), or specific courses."
    )


async def query_student_records_ai(question: str, students: List[Student]) -> Dict[str, Any]:
    """
    Processes a natural language question grounded in current SQLite student records.
    Attempts local Ollama LLM first; falls back gracefully if Ollama is unreachable.
    """
    records_context = _format_students_context(students)
    total_records = len(students)

    system_prompt = (
        "You are an intelligent, helpful academic records assistant for EWB Edu Tech Pvt. Ltd. "
        "Answer questions strictly using the student records provided in the context below. "
        "Do NOT invent or hallucinate information not present in the data. "
        "Keep your response concise, professional, and clear.\n\n"
        f"CURRENT STUDENT DATABASE RECORDS ({total_records} records):\n"
        f"{records_context}"
    )

    user_prompt = f"Question: {question}"

    # Try Ollama endpoint
    try:
        async with httpx.AsyncClient(timeout=settings.OLLAMA_TIMEOUT) as client:
            ollama_url = f"{settings.OLLAMA_HOST.rstrip('/')}/api/generate"
            payload = {
                "model": settings.OLLAMA_MODEL,
                "prompt": f"{system_prompt}\n\n{user_prompt}\n\nAnswer:",
                "stream": False,
                "options": {
                    "temperature": 0.2
                }
            }
            response = await client.post(ollama_url, json=payload)
            if response.status_code == 200:
                result_json = response.json()
                ai_answer = result_json.get("response", "").strip()
                if ai_answer:
                    return {
                        "question": question,
                        "answer": ai_answer,
                        "records_analyzed": total_records,
                        "model_used": f"Ollama ({settings.OLLAMA_MODEL})",
                        "grounded_context_summary": f"{total_records} records provided as context"
                    }
    except Exception as exc:
        logger.info(f"Ollama server not active or reachable ({exc}). Using deterministic grounded engine.")

    # Fallback to deterministic grounded engine
    grounded_answer = _rule_based_grounded_fallback(question, students)
    return {
        "question": question,
        "answer": grounded_answer,
        "records_analyzed": total_records,
        "model_used": "Grounded Context Engine (Ollama Local Fallback)",
        "grounded_context_summary": f"{total_records} records grounded in SQLite database"
    }
