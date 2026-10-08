from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.config import get_settings
from app.database import engine, Base
from app.routers import students, ai

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure database schema is created on startup
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "**Students Database CRUD Application** developed for Python Backend Development Internship "
        "at **EWB EDU TECH PVT. LTD.**\n\n"
        "### Key Features:\n"
        "- 📚 Full CRUD operations on student records with SQLite persistence\n"
        "- 🔍 Advanced filtering, pagination, and search\n"
        "- 🛡️ Robust Pydantic data validation & error handling\n"
        "- 🤖 Optional Bonus: Grounded Local AI queries powered by Ollama"
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for cross-origin frontend or testing clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(students.router)
app.include_router(ai.router)


@app.get("/", tags=["General"])
def root():
    return {
        "project": "Students Database CRUD Application",
        "organization": "EWB EDU TECH PVT. LTD.",
        "status": "online",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "endpoints": {
            "students_crud": "/students",
            "ai_natural_language_query": "/ai/query",
            "health_check": "/health"
        }
    }


@app.get("/health", tags=["General"])
def health_check():
    return {
        "status": "healthy",
        "database": "connected (SQLite)",
        "version": settings.APP_VERSION
    }
