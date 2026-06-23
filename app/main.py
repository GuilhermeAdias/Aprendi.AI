"""Ponto de entrada da aplicação Aprendi.AI (FastAPI).

Executar em desenvolvimento:
    uvicorn app.main:app --reload
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app import __version__
from app.core.templates import templates
from app.routers import admin, evaluation, game, pages, prompt_lab, quiz
from app.storage import json_storage

STATIC_DIR = Path(__file__).resolve().parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Garante a existência dos arquivos de dados ao iniciar a aplicação."""
    json_storage.ensure_storage()
    yield


app = FastAPI(
    title="Aprendi.AI",
    description="Plataforma educativa para ensinar Inteligência Artificial a crianças e adolescentes.",
    version=__version__,
    lifespan=lifespan,
)

# Arquivos estáticos (CSS e JS).
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Registro das rotas.
app.include_router(pages.router)
app.include_router(prompt_lab.router)
app.include_router(game.router)
app.include_router(quiz.router)
app.include_router(evaluation.router)
app.include_router(admin.router)


@app.exception_handler(404)
async def not_found(request: Request, exc):
    """Página 404 amigável."""
    return templates.TemplateResponse(
        "404.html", {"request": request}, status_code=404
    )


@app.get("/health", include_in_schema=False)
def health() -> dict:
    """Endpoint simples de verificação de saúde."""
    return {"status": "ok", "app": "Aprendi.AI", "version": __version__}
