"""Rotas da área administrativa (painel de resultados).

ATENÇÃO: esta área não possui autenticação, conforme o escopo acadêmico do
projeto. Em produção, ela deve ser protegida.
"""

from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.core.templates import templates
from app.services.statistics_service import StatisticsService

router = APIRouter()
_stats = StatisticsService()


@router.get("/admin/resultados", response_class=HTMLResponse)
def resultados(request: Request):
    report = _stats.full_report()
    return templates.TemplateResponse(
        "admin.html", {"request": request, "report": report}
    )
