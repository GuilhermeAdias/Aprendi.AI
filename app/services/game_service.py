"""Serviço do Jogo dos Prompts.

Controla as 6 missões (com complexidade crescente), o sorteio de questões por
dificuldade, o cálculo de XP e de estrelas (estilo Angry Birds) e a
persistência dos resultados em ``data/game_scores.json``.
"""

from __future__ import annotations

import random
from datetime import datetime, timezone

from app.data.missions import (
    DIFICULDADES,
    MISSIONS,
    QUESTOES_POR_MISSAO,
    XP_MAXIMO,
    XP_MINIMO_META,
)
from app.storage import json_storage

_IDS_DIFICULDADE = {d["id"] for d in DIFICULDADES}


class GameService:
    """Regras do jogo de missões sobre Inteligência Artificial."""

    def __init__(self) -> None:
        self.missions = MISSIONS
        self.questoes_por_missao = QUESTOES_POR_MISSAO
        self.xp_maximo = XP_MAXIMO
        self.xp_minimo_meta = XP_MINIMO_META
        self.estrelas_por_missao = 3

    # ----- Acesso a dados ------------------------------------------------
    def get_missions(self) -> list[dict]:
        return self.missions

    def get_difficulties(self) -> list[dict]:
        return DIFICULDADES

    def total_missions(self) -> int:
        return len(self.missions)

    def max_xp(self) -> int:
        """XP máximo possível (todos os acertos em todas as missões)."""
        return sum(m["xp_por_acerto"] * self.questoes_por_missao for m in self.missions)

    def max_estrelas(self) -> int:
        return self.total_missions() * self.estrelas_por_missao

    def _mission(self, mission_id: int) -> dict:
        mission = next((m for m in self.missions if m["id"] == mission_id), None)
        if mission is None:
            raise ValueError(f"Missão {mission_id} não encontrada.")
        return mission

    # ----- Sorteio de questões ------------------------------------------
    def select_questions(self, mission_id: int, dificuldade: str) -> list[dict]:
        """Sorteia as questões de uma missão para a dificuldade escolhida.

        Filtra o acervo pela dificuldade; se houver menos que o necessário,
        completa com questões de outras dificuldades.
        """
        if dificuldade not in _IDS_DIFICULDADE:
            raise ValueError(f"Dificuldade inválida: {dificuldade}")
        mission = self._mission(mission_id)
        pool = [q for q in mission["questoes"] if q["dificuldade"] == dificuldade]
        outras = [q for q in mission["questoes"] if q["dificuldade"] != dificuldade]
        random.shuffle(pool)
        random.shuffle(outras)
        selecionadas = pool[: self.questoes_por_missao]
        if len(selecionadas) < self.questoes_por_missao:
            faltam = self.questoes_por_missao - len(selecionadas)
            selecionadas += outras[:faltam]
        return selecionadas

    def build_game(self, dificuldade: str) -> list[dict]:
        """Monta uma partida completa: 6 missões com 5 questões cada."""
        partida = []
        for m in self.missions:
            partida.append(
                {
                    "id": m["id"],
                    "titulo": m["titulo"],
                    "descricao": m["descricao"],
                    "tema": m["tema"],
                    "icone": m["icone"],
                    "xp_por_acerto": m["xp_por_acerto"],
                    "questoes": self.select_questions(m["id"], dificuldade),
                }
            )
        return partida

    # ----- Pontuação -----------------------------------------------------
    def stars_for_correct(self, acertos: int) -> int:
        """Estrelas de uma missão conforme o número de acertos (de 5)."""
        if acertos >= 5:
            return 3
        if acertos >= 3:
            return 2
        if acertos >= 1:
            return 1
        return 0

    def compute_result(self, acertos_por_missao: list[int], dificuldade: str | None = None) -> dict:
        """Calcula XP, estrelas, percentual e mensagem da partida.

        ``acertos_por_missao`` é uma lista com o número de acertos em cada
        missão (na ordem das missões).
        """
        xp = 0
        estrelas = 0
        acertos_total = 0
        detalhes = []
        for indice, mission in enumerate(self.missions):
            acertos = 0
            if indice < len(acertos_por_missao):
                acertos = max(0, min(int(acertos_por_missao[indice]), self.questoes_por_missao))
            estrelas_missao = self.stars_for_correct(acertos)
            xp_missao = acertos * mission["xp_por_acerto"]
            xp += xp_missao
            estrelas += estrelas_missao
            acertos_total += acertos
            detalhes.append(
                {
                    "id": mission["id"],
                    "titulo": mission["titulo"],
                    "acertos": acertos,
                    "estrelas": estrelas_missao,
                    "xp": xp_missao,
                }
            )

        max_xp = self.max_xp()
        percent = round((xp / max_xp) * 100) if max_xp else 0
        passou = xp >= self.xp_minimo_meta
        return {
            "xp": xp,
            "max_xp": max_xp,
            "estrelas": estrelas,
            "max_estrelas": self.max_estrelas(),
            "acertos": acertos_total,
            "total_questoes": self.total_missions() * self.questoes_por_missao,
            "percent": percent,
            "passou": passou,
            "meta": self.xp_minimo_meta,
            "dificuldade": dificuldade,
            "detalhes": detalhes,
            "message": self._message(xp, passou),
        }

    def save_result(self, acertos_por_missao: list[int], dificuldade: str | None = None) -> dict:
        """Calcula e persiste o resultado de uma partida."""
        result = self.compute_result(acertos_por_missao, dificuldade)
        record = {
            "acertos": result["acertos"],
            "total": result["total_questoes"],
            "xp": result["xp"],
            "estrelas": result["estrelas"],
            "percent": result["percent"],
            "dificuldade": dificuldade,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        json_storage.append(json_storage.GAME_SCORES_FILE, record)
        return result

    def _message(self, xp: int, passou: bool) -> str:
        if xp >= self.xp_maximo:
            return "PERFEITO! 2000 XP! Você é a lenda dos prompts! 🏆🔥"
        if xp >= 1500:
            return "Incrível! Você dominou a Inteligência Artificial! 🌟"
        if xp >= 1000:
            return "Muito bom! Você manda bem em IA! 💪"
        if passou:
            return "Boa! Você bateu a meta de 500 XP! Continue evoluindo. 🚀"
        return "Quase lá! Você precisa de 500 XP para vencer. Revise e tente de novo! 🌱"
