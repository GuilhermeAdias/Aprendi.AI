"""Serviço do Quiz educativo.

Controla as perguntas, a correção das respostas, o cálculo da pontuação e a
persistência dos resultados em ``data/quiz_scores.json``.
"""

from __future__ import annotations

from datetime import datetime, timezone

from app.data.quiz_questions import QUIZ_QUESTIONS, XP_POR_ACERTO
from app.storage import json_storage


class QuizService:
    """Regras do quiz de Inteligência Artificial."""

    def __init__(self) -> None:
        self.questions = QUIZ_QUESTIONS
        self.xp_por_acerto = XP_POR_ACERTO

    def get_questions(self) -> list[dict]:
        return self.questions

    def total_questions(self) -> int:
        return len(self.questions)

    def correct_answer(self, question_id: int) -> int:
        question = next((q for q in self.questions if q["id"] == question_id), None)
        if question is None:
            raise ValueError(f"Pergunta {question_id} não encontrada.")
        return question["correta"]

    def score_answers(self, answers: dict[int, int]) -> dict:
        """Corrige um conjunto de respostas.

        ``answers`` mapeia ``question_id`` -> índice da alternativa escolhida.
        Retorna pontuação, total, percentual e mensagem personalizada.
        """
        correct = 0
        details: list[dict] = []
        for question in self.questions:
            qid = question["id"]
            chosen = answers.get(qid)
            is_correct = chosen is not None and int(chosen) == question["correta"]
            if is_correct:
                correct += 1
            details.append(
                {
                    "id": qid,
                    "chosen": chosen,
                    "correct_index": question["correta"],
                    "is_correct": is_correct,
                    "explicacao": question["explicacao"],
                }
            )
        return self._build_result(correct, details)

    def compute_score(self, correct_answers: int) -> dict:
        """Calcula o resultado a partir apenas do número de acertos."""
        total = self.total_questions()
        correct_answers = max(0, min(correct_answers, total))
        return self._build_result(correct_answers, details=None)

    def _build_result(self, correct: int, details: list[dict] | None) -> dict:
        total = self.total_questions()
        percent = round((correct / total) * 100) if total else 0
        result = {
            "correct": correct,
            "total": total,
            "percent": percent,
            "xp": correct * self.xp_por_acerto,
            "message": self._message_for_percent(percent),
        }
        if details is not None:
            result["details"] = details
        return result

    def save_result(self, correct_answers: int) -> dict:
        """Calcula e persiste o resultado de um quiz."""
        result = self.compute_score(correct_answers)
        record = {
            "correct": result["correct"],
            "total": result["total"],
            "percent": result["percent"],
            "xp": result["xp"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        json_storage.append(json_storage.QUIZ_SCORES_FILE, record)
        return result

    @staticmethod
    def _message_for_percent(percent: int) -> str:
        if percent >= 90:
            return "Uau! Você é um expert em Inteligência Artificial! 🧠🏆"
        if percent >= 70:
            return "Muito bom! Você entende bastante sobre IA! 🌟"
        if percent >= 50:
            return "Boa! Você está no caminho certo. Revise e tente de novo! 💪"
        return "Tudo bem! Explore as páginas e refaça o quiz para aprender mais. 🚀"
