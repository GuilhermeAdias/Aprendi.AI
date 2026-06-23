"""Rotas do Jogo dos Prompts."""

from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.core.templates import templates
from app.services.game_service import GameService

router = APIRouter()
_game = GameService()


class GameResult(BaseModel):
    correct: int = 0


@router.get("/jogo", response_class=HTMLResponse)
def jogo(request: Request):
    return templates.TemplateResponse(
        "jogo.html",
        {
            "request": request,
            "missions": _game.get_missions(),
            "total": _game.total_missions(),
            "xp_por_acerto": _game.xp_por_acerto,
            "max_xp": _game.max_xp(),
        },
    )


@router.post("/jogo/resultado")
def salvar_resultado(payload: GameResult):
    """Salva o resultado de uma partida e devolve a pontuação calculada."""
    return _game.save_result(payload.correct)
