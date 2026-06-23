"""Rotas da Avaliação (questionário de satisfação)."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse

from app.core.templates import templates
from app.storage import json_storage

router = APIRouter()


def _clamp(value: int) -> int:
    """Garante que a nota fique entre 1 e 5."""
    return max(1, min(5, value))


@router.get("/avaliacao", response_class=HTMLResponse)
def avaliacao(request: Request):
    return templates.TemplateResponse(
        "avaliacao.html", {"request": request, "enviado": False}
    )


@router.post("/avaliacao", response_class=HTMLResponse)
def enviar_avaliacao(
    request: Request,
    facilidade: int = Form(...),
    entendeu_ia: int = Form(...),
    aprendeu_prompts: int = Form(...),
    jogo_ajudou: int = Form(...),
    entendeu_erro: int = Form(...),
    comentario: str = Form(""),
):
    """Recebe a avaliação, salva em JSON e mostra a confirmação."""
    record = {
        "facilidade": _clamp(facilidade),
        "entendeu_ia": _clamp(entendeu_ia),
        "aprendeu_prompts": _clamp(aprendeu_prompts),
        "jogo_ajudou": _clamp(jogo_ajudou),
        "entendeu_erro": _clamp(entendeu_erro),
        "comentario": (comentario or "").strip()[:1000],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    json_storage.append(json_storage.EVALUATIONS_FILE, record)
    return templates.TemplateResponse(
        "avaliacao.html", {"request": request, "enviado": True}
    )
