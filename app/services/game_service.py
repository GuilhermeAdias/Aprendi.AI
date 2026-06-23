"""Serviço do Jogo dos Prompts.

Controla as missões, o cálculo de XP/pontuação e a persistência dos
resultados das partidas em ``data/game_scores.json``.
"""

from __future__ import annotations

from datetime import datetime, timezone

from app.data.missions import MISSIONS, XP_POR_ACERTO
from app.storage import json_storage


class GameService:
    """Regras do jogo de missões de prompts."""

    def __init__(self) -> None:
        self.missions = MISSIONS
        self.xp_por_acerto = XP_POR_ACERTO

    def get_missions(self) -> list[dict]:
        """Retorna a lista de missões do jogo."""
        return self.missions

    def total_missions(self) -> int:
        return len(self.missions)

    def max_xp(self) -> int:
        return len(self.missions) * self.xp_por_acerto

    def evaluate_answer(self, mission_id: int, chosen_index: int) -> dict:
        """Avalia uma única resposta de missão.

        Retorna se acertou, o XP ganho e a explicação.
        """
        mission = next((m for m in self.missions if m["id"] == mission_id), None)
        if mission is None:
            raise ValueError(f"Missão {mission_id} não encontrada.")
        correct = chosen_index == mission["correta"]
        return {
            "mission_id": mission_id,
            "correct": correct,
            "correct_index": mission["correta"],
            "xp": self.xp_por_acerto if correct else 0,
            "explicacao": mission["explicacao"],
        }

    def compute_score(self, correct_answers: int) -> dict:
        """Calcula XP, total e percentual a partir do número de acertos."""
        total = self.total_missions()
        correct_answers = max(0, min(correct_answers, total))
        xp = correct_answers * self.xp_por_acerto
        percent = round((correct_answers / total) * 100) if total else 0
        return {
            "correct": correct_answers,
            "total": total,
            "xp": xp,
            "max_xp": self.max_xp(),
            "percent": percent,
            "message": self._message_for_percent(percent),
        }

    def save_result(self, correct_answers: int) -> dict:
        """Calcula e persiste o resultado de uma partida."""
        result = self.compute_score(correct_answers)
        record = {
            "correct": result["correct"],
            "total": result["total"],
            "xp": result["xp"],
            "percent": result["percent"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        json_storage.append(json_storage.GAME_SCORES_FILE, record)
        return result

    @staticmethod
    def _message_for_percent(percent: int) -> str:
        if percent >= 100:
            return "Incrível! Você é um verdadeiro Mestre dos Prompts! 🏆"
        if percent >= 70:
            return "Muito bem! Você já cria prompts ótimos! 🌟"
        if percent >= 40:
            return "Bom trabalho! Continue praticando para evoluir. 💪"
        return "Você começou a jornada! Revise o Guia de Prompts e tente de novo. 🚀"
