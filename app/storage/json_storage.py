"""Utilitário de persistência em arquivos JSON.

Esta camada isola toda a leitura/escrita em disco do restante da aplicação.
Nenhum banco de dados é utilizado: os dados ficam em arquivos JSON dentro da
pasta ``data/`` na raiz do projeto. Os arquivos são criados automaticamente
caso ainda não existam.
"""

from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Any

# Raiz do projeto: este arquivo está em app/storage/json_storage.py,
# portanto parents[2] aponta para a pasta raiz do repositório.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"

# Arquivos de persistência usados pela aplicação.
EVALUATIONS_FILE = "evaluations.json"
GAME_SCORES_FILE = "game_scores.json"
QUIZ_SCORES_FILE = "quiz_scores.json"

# Cada arquivo guarda uma lista de registros.
_DEFAULT_CONTENT: dict[str, Any] = {
    EVALUATIONS_FILE: [],
    GAME_SCORES_FILE: [],
    QUIZ_SCORES_FILE: [],
}

# Trava simples para evitar corrida em escritas concorrentes (FastAPI pode
# atender requisições em paralelo).
_lock = threading.Lock()


def _path(filename: str) -> Path:
    """Retorna o caminho absoluto de um arquivo de dados."""
    return DATA_DIR / filename


def ensure_storage() -> None:
    """Garante que a pasta de dados e os arquivos JSON existam."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for filename, default in _DEFAULT_CONTENT.items():
        path = _path(filename)
        if not path.exists():
            _write_raw(path, default)


def _write_raw(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load(filename: str) -> list[dict[str, Any]]:
    """Carrega o conteúdo de um arquivo JSON como lista de registros.

    Se o arquivo não existir ou estiver corrompido/vazio, retorna o conteúdo
    padrão (lista vazia) sem lançar exceção.
    """
    path = _path(filename)
    if not path.exists():
        return list(_DEFAULT_CONTENT.get(filename, []))
    try:
        content = path.read_text(encoding="utf-8").strip()
        if not content:
            return []
        data = json.loads(content)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save(filename: str, data: list[dict[str, Any]]) -> None:
    """Salva (sobrescreve) a lista completa de registros em um arquivo."""
    with _lock:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        _write_raw(_path(filename), data)


def append(filename: str, record: dict[str, Any]) -> dict[str, Any]:
    """Adiciona um registro ao arquivo e retorna o próprio registro salvo."""
    with _lock:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        records = load(filename)
        records.append(record)
        _write_raw(_path(filename), records)
    return record
