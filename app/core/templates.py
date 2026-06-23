"""Configuração compartilhada do mecanismo de templates Jinja2."""

from __future__ import annotations

from pathlib import Path

from fastapi.templating import Jinja2Templates

# Diretório de templates: app/templates
TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Variáveis globais disponíveis em todos os templates.
templates.env.globals["app_name"] = "Aprendi.AI"
templates.env.globals["slogan"] = (
    "Aprenda Inteligência Artificial brincando, explorando e criando bons prompts."
)

# Itens de navegação reutilizados pelo cabeçalho e pelos cards da home.
NAV_ITEMS = [
    {"href": "/historia", "titulo": "História da IA", "icone": "📜",
     "descricao": "A jornada da Inteligência Artificial até hoje."},
    {"href": "/como-funciona", "titulo": "Como funciona", "icone": "⚙️",
     "descricao": "Entenda de forma simples como a IA aprende."},
    {"href": "/dia-a-dia", "titulo": "IA no dia a dia", "icone": "🌍",
     "descricao": "Onde a IA já está na sua rotina."},
    {"href": "/prompts", "titulo": "Guia de Prompts", "icone": "✍️",
     "descricao": "Aprenda a escrever pedidos incríveis para a IA."},
    {"href": "/laboratorio", "titulo": "Laboratório", "icone": "🧪",
     "descricao": "Teste seu prompt e receba uma nota na hora."},
    {"href": "/jogo", "titulo": "Jogo dos Prompts", "icone": "🎮",
     "descricao": "Cumpra missões e ganhe XP escolhendo bons prompts."},
    {"href": "/quiz", "titulo": "Quiz", "icone": "❓",
     "descricao": "Teste o que você aprendeu sobre IA."},
    {"href": "/seguranca", "titulo": "Segurança", "icone": "🛡️",
     "descricao": "Use a IA de forma segura e responsável."},
    {"href": "/sobre", "titulo": "Sobre", "icone": "ℹ️",
     "descricao": "Conheça o projeto Aprendi.AI."},
]

templates.env.globals["nav_items"] = NAV_ITEMS
