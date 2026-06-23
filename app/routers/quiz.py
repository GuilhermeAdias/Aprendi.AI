"""Rotas do Quiz educativo."""

from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.core.templates import templates
from app.services.quiz_service import QuizService

router = APIRouter()
_quiz = QuizService()


class QuizResult(BaseModel):
    correct: int = 0


@router.get("/quiz", response_class=HTMLResponse)
def quiz(request: Request):
    return templates.TemplateResponse(
        "quiz.html",
        {
            "request": request,
            "questions": _quiz.get_questions(),
            "total": _quiz.total_questions(),
            "xp_por_acerto": _quiz.xp_por_acerto,
        },
    )


@router.post("/quiz/resultado")
def salvar_resultado(payload: QuizResult):
    """Salva o resultado de um quiz e devolve a pontuação calculada."""
    return _quiz.save_result(payload.correct)
