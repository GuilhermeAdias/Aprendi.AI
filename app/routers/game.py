"""Rotas dos Games: central, Jogo dos Prompts, Monte o Prompt e Real ou IA?."""

from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.core.templates import templates
from app.data.build_prompt import DESAFIOS, XP_POR_ACERTO as MONTAR_XP
from app.data.real_or_ai import ITENS, XP_POR_ACERTO as REAL_XP
from app.services.game_service import GameService

router = APIRouter()
_game = GameService()

# Metadados dos games para a central /games.
GAMES = [
    {"href": "/jogo", "titulo": "Jogo dos Prompts", "icone": "🎮",
     "descricao": "6 missões com complexidade crescente. Ganhe XP e estrelas!",
     "cor": "from-marca-azul to-marca-roxo"},
    {"href": "/montar-prompt", "titulo": "Monte o Prompt", "icone": "🧩",
     "descricao": "Monte o melhor prompt escolhendo os blocos certos.",
     "cor": "from-marca-roxo to-marca-roxoclaro"},
    {"href": "/real-ou-ia", "titulo": "Real ou IA?", "icone": "🕵️",
     "descricao": "Adivinhe se foi feito por um humano ou por uma IA.",
     "cor": "from-marca-azulclaro to-marca-azul"},
]


class GameResult(BaseModel):
    acertos_por_missao: list[int] = []
    dificuldade: str | None = None


@router.get("/games", response_class=HTMLResponse)
def games(request: Request):
    return templates.TemplateResponse("games.html", {"request": request, "games": GAMES})


# ----- Jogo dos Prompts --------------------------------------------------
@router.get("/jogo", response_class=HTMLResponse)
def jogo(request: Request):
    return templates.TemplateResponse(
        "jogo.html",
        {
            "request": request,
            "missions": _game.get_missions(),
            "difficulties": _game.get_difficulties(),
            "questoes_por_missao": _game.questoes_por_missao,
            "max_xp": _game.max_xp(),
            "meta": _game.xp_minimo_meta,
            "max_estrelas": _game.max_estrelas(),
        },
    )


@router.post("/jogo/resultado")
def salvar_resultado(payload: GameResult):
    """Salva o resultado de uma partida e devolve a pontuação calculada."""
    return _game.save_result(payload.acertos_por_missao, payload.dificuldade)


# ----- Monte o Prompt ----------------------------------------------------
@router.get("/montar-prompt", response_class=HTMLResponse)
def montar_prompt(request: Request):
    return templates.TemplateResponse(
        "montar_prompt.html",
        {"request": request, "desafios": DESAFIOS, "xp_por_acerto": MONTAR_XP},
    )


# ----- Real ou IA? -------------------------------------------------------
@router.get("/real-ou-ia", response_class=HTMLResponse)
def real_ou_ia(request: Request):
    return templates.TemplateResponse(
        "real_ou_ia.html",
        {"request": request, "itens": ITENS, "xp_por_acerto": REAL_XP},
    )
