"""Serviço de análise de prompts (Laboratório de Prompts).

A análise é baseada em regras reais (não em IA externa). Avalia o prompt do
usuário em sete critérios e devolve uma pontuação de 0 a 100, um nível, os
pontos fortes, sugestões de melhoria e uma versão melhorada do prompt.
"""

from __future__ import annotations

import re
import unicodedata

# Cada critério contribui com um peso para a pontuação final (soma = 100).
_CRITERIA_WEIGHTS = {
    "objetivo": 22,
    "contexto": 16,
    "formato": 14,
    "publico": 12,
    "tom": 8,
    "clareza": 16,
    "tamanho": 12,
}

# Palavras que indicam cada critério dentro do prompt.
_OBJETIVO_KEYWORDS = [
    "explique", "explica", "crie", "criar", "faca", "faça", "escreva",
    "resuma", "resumir", "liste", "lista", "compare", "descreva", "monte",
    "gere", "gerar", "ensine", "ensina", "ajude", "ajuda", "traduza",
    "calcule", "mostre", "sugira", "sugerir", "como",
]
_CONTEXTO_KEYWORDS = [
    "sou", "estou", "tenho", "preciso", "quero", "minha", "meu", "para a prova",
    "trabalho", "escola", "professor", "redacao", "redação", "tema", "porque",
    "ano", "serie", "série", "contexto", "situacao", "situação",
]
_FORMATO_KEYWORDS = [
    "topicos", "tópicos", "lista", "tabela", "passo a passo", "passos",
    "linhas", "paragrafo", "parágrafo", "itens", "exemplo", "exemplos",
    "frases", "formato", "em ", "bullet",
]
_PUBLICO_KEYWORDS = [
    "crianca", "criança", "aluno", "estudante", "anos", "iniciante",
    "como se eu tivesse", "para um", "para uma", "publico", "público",
    "leigo", "professor", "9o", "9º", "7o", "7º", "8o", "8º",
]
_TOM_KEYWORDS = [
    "divertido", "divertida", "engracado", "engraçado", "serio", "sério",
    "formal", "informal", "simples", "carinhoso", "motivador", "amigavel",
    "amigável", "tom", "linguagem", "facil", "fácil",
]


def _strip_accents(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(c for c in normalized if not unicodedata.combining(c))


def _contains_any(text_norm: str, keywords: list[str]) -> bool:
    for kw in keywords:
        kw_norm = _strip_accents(kw.lower())
        if kw_norm in text_norm:
            return True
    return False


class PromptAnalyzerService:
    """Analisa a qualidade de um prompt usando regras explícitas."""

    def analyze(self, prompt: str) -> dict:
        """Analisa o prompt e retorna o resultado estruturado.

        Retorno:
            {
                "score": int (0-100),
                "level": str,
                "strengths": list[str],
                "improvements": list[str],
                "suggested_prompt": str,
            }
        """
        prompt = (prompt or "").strip()
        text_norm = _strip_accents(prompt.lower())
        words = re.findall(r"\b\w+\b", prompt)
        word_count = len(words)

        strengths: list[str] = []
        improvements: list[str] = []
        score = 0

        # --- Critério: prompt vazio --------------------------------------
        if word_count == 0:
            return {
                "score": 0,
                "level": "Vazio",
                "strengths": [],
                "improvements": [
                    "Você não escreveu nada! Comece dizendo o que você quer que a IA faça.",
                ],
                "suggested_prompt": (
                    "Explique de forma simples o que é Inteligência Artificial "
                    "para um estudante de 12 anos, em 4 tópicos curtos."
                ),
            }

        # --- Critério: objetivo ------------------------------------------
        has_objetivo = _contains_any(text_norm, _OBJETIVO_KEYWORDS)
        if has_objetivo:
            score += _CRITERIA_WEIGHTS["objetivo"]
            strengths.append("Tem um objetivo claro (você diz o que quer que a IA faça). 🎯")
        else:
            improvements.append(
                "Diga o objetivo com um verbo de ação no começo: 'Explique', 'Crie', 'Resuma'..."
            )

        # --- Critério: contexto ------------------------------------------
        has_contexto = _contains_any(text_norm, _CONTEXTO_KEYWORDS)
        if has_contexto:
            score += _CRITERIA_WEIGHTS["contexto"]
            strengths.append("Dá contexto sobre a sua situação. 🧩")
        else:
            improvements.append(
                "Inclua um contexto: conte quem você é ou para que serve (ex.: 'sou aluno do 7º ano')."
            )

        # --- Critério: formato -------------------------------------------
        has_formato = _contains_any(text_norm, _FORMATO_KEYWORDS)
        if has_formato:
            score += _CRITERIA_WEIGHTS["formato"]
            strengths.append("Indica o formato da resposta (lista, tópicos, tabela...). 📋")
        else:
            improvements.append(
                "Peça um formato: 'em 5 tópicos', 'em uma tabela' ou 'em 3 frases'."
            )

        # --- Critério: público -------------------------------------------
        has_publico = _contains_any(text_norm, _PUBLICO_KEYWORDS)
        if has_publico:
            score += _CRITERIA_WEIGHTS["publico"]
            strengths.append("Define o público (para quem é a resposta). 👥")
        else:
            improvements.append(
                "Diga para quem é: 'explique como se eu tivesse 10 anos'."
            )

        # --- Critério: tom -----------------------------------------------
        has_tom = _contains_any(text_norm, _TOM_KEYWORDS)
        if has_tom:
            score += _CRITERIA_WEIGHTS["tom"]
            strengths.append("Escolhe um tom ou estilo para a resposta. 🎭")
        else:
            improvements.append(
                "Escolha um tom: 'de forma divertida', 'simples' ou 'como um professor'."
            )

        # --- Critério: clareza -------------------------------------------
        # Penaliza prompts em letras maiúsculas gritando, sem pontuação ou
        # cheios de abreviações como "vc", "pq".
        clareza_ok = True
        abreviacoes = [" vc ", " pq ", " td ", " mt ", " blz ", " kkk "]
        text_spaced = f" {text_norm} "
        if any(ab in text_spaced for ab in abreviacoes):
            clareza_ok = False
        if word_count >= 3 and prompt.isupper():
            clareza_ok = False
        if clareza_ok:
            score += _CRITERIA_WEIGHTS["clareza"]
            strengths.append("Está escrito de forma clara e sem abreviações confusas. ✨")
        else:
            improvements.append(
                "Escreva por extenso e sem gírias/abreviações (evite 'vc', 'pq') para a IA entender melhor."
            )

        # --- Critério: tamanho -------------------------------------------
        # Prompts muito curtos costumam ser vagos; muito longos podem confundir.
        if word_count < 4:
            improvements.append(
                "Seu prompt está muito curto. Adicione mais detalhes para a IA entender o que você quer."
            )
        elif word_count > 120:
            score += _CRITERIA_WEIGHTS["tamanho"] // 2
            improvements.append(
                "Seu prompt está bem longo. Tente deixar mais direto, mantendo só o essencial."
            )
        else:
            score += _CRITERIA_WEIGHTS["tamanho"]
            strengths.append("Tem um tamanho equilibrado: nem curto demais, nem longo demais. 📏")

        score = max(0, min(100, score))
        level = self._level_for_score(score)
        suggested_prompt = self._build_suggested_prompt(
            prompt,
            has_objetivo=has_objetivo,
            has_contexto=has_contexto,
            has_formato=has_formato,
            has_publico=has_publico,
            has_tom=has_tom,
        )

        if not strengths:
            strengths.append("Você começou a praticar — esse já é o primeiro passo! 👏")

        return {
            "score": score,
            "level": level,
            "strengths": strengths,
            "improvements": improvements,
            "suggested_prompt": suggested_prompt,
        }

    @staticmethod
    def _level_for_score(score: int) -> str:
        if score >= 85:
            return "Mestre dos Prompts"
        if score >= 70:
            return "Avançado"
        if score >= 50:
            return "Intermediário"
        if score >= 30:
            return "Aprendiz"
        return "Iniciante"

    @staticmethod
    def _build_suggested_prompt(
        prompt: str,
        *,
        has_objetivo: bool,
        has_contexto: bool,
        has_formato: bool,
        has_publico: bool,
        has_tom: bool,
    ) -> str:
        """Monta uma versão melhorada do prompt acrescentando o que faltou."""
        base = prompt.rstrip(" .")
        extras: list[str] = []

        if not has_objetivo:
            base = f"Explique {base}" if base else "Explique o tema escolhido"
        if not has_contexto:
            extras.append("considerando que sou um estudante")
        if not has_publico:
            extras.append("com linguagem para um jovem de 12 anos")
        if not has_formato:
            extras.append("em 4 tópicos curtos")
        if not has_tom:
            extras.append("de forma simples e divertida")

        suggestion = base
        if extras:
            suggestion = f"{base}, " + ", ".join(extras)
        suggestion = suggestion.strip()
        if not suggestion.endswith("."):
            suggestion += "."
        # Garante a primeira letra maiúscula.
        return suggestion[0].upper() + suggestion[1:] if suggestion else suggestion
