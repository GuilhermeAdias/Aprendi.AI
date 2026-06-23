"""Rotas do Laboratório de Prompts."""

from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.core.templates import templates
from app.services.prompt_analyzer import PromptAnalyzerService

router = APIRouter()
_analyzer = PromptAnalyzerService()


class PromptRequest(BaseModel):
    prompt: str = ""


@router.get("/laboratorio", response_class=HTMLResponse)
def laboratorio(request: Request):
    return templates.TemplateResponse("laboratorio.html", {"request": request})


@router.post("/laboratorio/analisar")
def analisar(payload: PromptRequest):
    """Analisa um prompt e retorna o resultado em JSON."""
    return _analyzer.analyze(payload.prompt)
