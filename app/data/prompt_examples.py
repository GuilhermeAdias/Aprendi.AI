"""Exemplos e fundamentos para o Guia de Prompts.

Inclui os 6 ingredientes de um bom prompt e exemplos de prompts ruins
melhorados, em linguagem acessível para crianças e adolescentes.
"""

from __future__ import annotations

# Os 6 ingredientes de um bom prompt.
PROMPT_INGREDIENTS: list[dict[str, str]] = [
    {
        "nome": "Objetivo",
        "icone": "🎯",
        "texto": "Diga claramente o que você quer. Ex.: 'Explique', 'Crie uma lista', 'Resuma'.",
    },
    {
        "nome": "Contexto",
        "icone": "🧩",
        "texto": "Conte a situação. Ex.: 'Sou estudante do 7º ano e tenho uma prova amanhã'.",
    },
    {
        "nome": "Formato",
        "icone": "📋",
        "texto": "Diga como quer a resposta. Ex.: 'em tópicos', 'em uma tabela', 'em 3 frases'.",
    },
    {
        "nome": "Público",
        "icone": "👥",
        "texto": "Diga para quem é. Ex.: 'explique como se eu tivesse 10 anos'.",
    },
    {
        "nome": "Restrições",
        "icone": "🚧",
        "texto": "Coloque limites. Ex.: 'use no máximo 5 linhas' ou 'sem palavras difíceis'.",
    },
    {
        "nome": "Tom",
        "icone": "🎭",
        "texto": "Escolha o estilo. Ex.: 'de forma divertida', 'séria', 'como um professor'.",
    },
]

# Exemplos de prompts ruins e suas versões melhoradas.
PROMPT_EXAMPLES: list[dict[str, str]] = [
    {
        "ruim": "fala sobre planetas",
        "bom": (
            "Explique para um estudante de 11 anos quais são os planetas do "
            "Sistema Solar, em uma lista com uma curiosidade divertida sobre "
            "cada um. Use no máximo 8 itens e linguagem simples."
        ),
        "porque": (
            "O prompt melhorado tem objetivo (explicar), público (11 anos), "
            "formato (lista) e restrição (até 8 itens)."
        ),
    },
    {
        "ruim": "me ajuda na redação",
        "bom": (
            "Sou estudante do 9º ano e preciso escrever uma redação sobre "
            "reciclagem. Me dê 3 ideias de argumentos e um exemplo de "
            "introdução curta, com tom motivador."
        ),
        "porque": (
            "Agora há contexto (9º ano, tema reciclagem), objetivo (ideias e "
            "introdução), formato (3 argumentos) e tom (motivador)."
        ),
    },
    {
        "ruim": "conta uma historia",
        "bom": (
            "Crie uma história curta e divertida, de no máximo 10 linhas, "
            "sobre um robô que aprende a fazer amigos na escola. O público é "
            "uma criança de 9 anos."
        ),
        "porque": (
            "Define objetivo (história), restrição (10 linhas), tema (robô e "
            "amizade), público (9 anos) e tom (divertido)."
        ),
    },
    {
        "ruim": "explica matematica",
        "bom": (
            "Explique de forma simples como somar frações com denominadores "
            "diferentes. Mostre um exemplo passo a passo, como se eu tivesse "
            "12 anos, em até 6 linhas."
        ),
        "porque": (
            "Tem objetivo (explicar soma de frações), formato (passo a passo "
            "com exemplo), público (12 anos) e restrição (6 linhas)."
        ),
    },
]
