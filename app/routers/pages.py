"""Rotas das páginas de conteúdo (sem formulários dinâmicos)."""

from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.core.templates import templates
from app.data.ai_examples import AI_EXAMPLES
from app.data.prompt_examples import PROMPT_EXAMPLES, PROMPT_INGREDIENTS
from app.data.timeline import TIMELINE

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/historia", response_class=HTMLResponse)
def historia(request: Request):
    return templates.TemplateResponse(
        "historia.html", {"request": request, "timeline": TIMELINE}
    )


@router.get("/como-funciona", response_class=HTMLResponse)
def como_funciona(request: Request):
    return templates.TemplateResponse("como_funciona.html", {"request": request})


@router.get("/dia-a-dia", response_class=HTMLResponse)
def dia_a_dia(request: Request):
    return templates.TemplateResponse(
        "dia_a_dia.html", {"request": request, "examples": AI_EXAMPLES}
    )


@router.get("/prompts", response_class=HTMLResponse)
def prompts(request: Request):
    return templates.TemplateResponse(
        "prompts.html",
        {
            "request": request,
            "ingredients": PROMPT_INGREDIENTS,
            "examples": PROMPT_EXAMPLES,
        },
    )


@router.get("/seguranca", response_class=HTMLResponse)
def seguranca(request: Request):
    return templates.TemplateResponse("seguranca.html", {"request": request})


@router.get("/sobre", response_class=HTMLResponse)
def sobre(request: Request):
    return templates.TemplateResponse("sobre.html", {"request": request})
