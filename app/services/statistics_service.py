"""Serviço de estatísticas (área administrativa).

Agrega os dados persistidos nos arquivos JSON para alimentar o painel
``/admin/resultados``: médias das avaliações, totais de quizzes e partidas,
médias de pontuação e comentários.
"""

from __future__ import annotations

from app.storage import json_storage

# Perguntas da avaliação (escala 1-5). As chaves correspondem aos campos
# salvos em evaluations.json.
EVALUATION_FIELDS = [
    ("facilidade", "Facilidade de uso"),
    ("entendeu_ia", "Entendeu o que é IA"),
    ("aprendeu_prompts", "Aprendeu sobre prompts"),
    ("jogo_ajudou", "O jogo ajudou no aprendizado"),
    ("entendeu_erro", "Entendeu que a IA pode errar"),
]


class StatisticsService:
    """Gera agregações a partir dos arquivos de dados."""

    def _average(self, values: list[float]) -> float:
        return round(sum(values) / len(values), 2) if values else 0.0

    def evaluation_stats(self, evaluations: list[dict] | None = None) -> dict:
        """Calcula totais, médias por pergunta e lista de comentários."""
        if evaluations is None:
            evaluations = json_storage.load(json_storage.EVALUATIONS_FILE)

        total = len(evaluations)
        averages: list[dict] = []
        for key, label in EVALUATION_FIELDS:
            values = [
                float(e[key])
                for e in evaluations
                if isinstance(e.get(key), (int, float))
            ]
            averages.append(
                {
                    "key": key,
                    "label": label,
                    "average": self._average(values),
                    "responses": len(values),
                }
            )

        comments = [
            {
                "texto": e["comentario"].strip(),
                "timestamp": e.get("timestamp", ""),
            }
            for e in evaluations
            if isinstance(e.get("comentario"), str) and e.get("comentario", "").strip()
        ]

        # Média geral de satisfação (média das médias com respostas).
        scored = [a["average"] for a in averages if a["responses"] > 0]
        overall = self._average(scored) if scored else 0.0

        return {
            "total": total,
            "averages": averages,
            "comments": comments,
            "overall_average": overall,
        }

    def quiz_stats(self, scores: list[dict] | None = None) -> dict:
        if scores is None:
            scores = json_storage.load(json_storage.QUIZ_SCORES_FILE)
        total = len(scores)
        percents = [float(s["percent"]) for s in scores if "percent" in s]
        correct = [float(s["correct"]) for s in scores if "correct" in s]
        return {
            "total": total,
            "average_percent": self._average(percents),
            "average_correct": self._average(correct),
        }

    def game_stats(self, scores: list[dict] | None = None) -> dict:
        if scores is None:
            scores = json_storage.load(json_storage.GAME_SCORES_FILE)
        total = len(scores)
        percents = [float(s["percent"]) for s in scores if "percent" in s]
        xps = [float(s["xp"]) for s in scores if "xp" in s]
        return {
            "total": total,
            "average_percent": self._average(percents),
            "average_xp": self._average(xps),
        }

    def full_report(self) -> dict:
        """Relatório completo usado pela página de administração."""
        return {
            "evaluation": self.evaluation_stats(),
            "quiz": self.quiz_stats(),
            "game": self.game_stats(),
        }
