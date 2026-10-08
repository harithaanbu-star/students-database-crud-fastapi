from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AIQueryRequest, AIQueryResponse
from app import crud
from app.ai_service import query_student_records_ai

router = APIRouter(
    prefix="/ai",
    tags=["AI Assistant (Ollama Extension)"]
)


@router.post(
    "/query",
    response_model=AIQueryResponse,
    status_code=status.HTTP_200_OK,
    summary="Ask natural language questions about student data",
    description=(
        "Optional Bonus AI feature: Receives a question, retrieves stored student records from SQLite, "
        "and produces a grounded, human-readable response using a local Ollama model (or intelligent grounded fallback)."
    )
)
async def ask_ai_question(
    request: AIQueryRequest,
    db: Session = Depends(get_db)
):
    # Fetch safe student records to ground LLM context
    students = crud.get_all_students_for_ai(db, limit=200)
    result = await query_student_records_ai(request.question, students)
    return AIQueryResponse(**result)
