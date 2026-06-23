"""Dados do game 'Monte o Prompt'.

O jogador recebe um cenário e monta o melhor prompt escolhendo um bloco em
cada categoria (Objetivo, Contexto, Formato, Tom). Em cada categoria há uma
opção que é a melhor escolha. Ao final, o prompt montado é exibido.
"""

from __future__ import annotations

XP_POR_ACERTO = 25  # XP por bloco "melhor" escolhido

DESAFIOS: list[dict] = [
    {
        "id": 1,
        "cenario": "Você tem prova de Ciências e quer entender a fotossíntese.",
        "categorias": [
            {"nome": "Objetivo", "icone": "🎯", "opcoes": [
                {"texto": "Explique a fotossíntese", "bom": True},
                {"texto": "planta", "bom": False},
                {"texto": "oi", "bom": False},
            ]},
            {"nome": "Público", "icone": "👤", "opcoes": [
                {"texto": "para um aluno de 11 anos", "bom": True},
                {"texto": "para um cientista PhD", "bom": False},
                {"texto": "para um robô", "bom": False},
            ]},
            {"nome": "Formato", "icone": "📋", "opcoes": [
                {"texto": "em 4 tópicos simples", "bom": True},
                {"texto": "em 20 páginas", "bom": False},
                {"texto": "sem organização", "bom": False},
            ]},
            {"nome": "Tom", "icone": "🎭", "opcoes": [
                {"texto": "de forma divertida", "bom": True},
                {"texto": "bem complicada", "bom": False},
                {"texto": "com palavras difíceis", "bom": False},
            ]},
        ],
    },
    {
        "id": 2,
        "cenario": "Você quer uma história curta para contar ao seu irmão de 6 anos.",
        "categorias": [
            {"nome": "Objetivo", "icone": "🎯", "opcoes": [
                {"texto": "Crie uma história curta", "bom": True},
                {"texto": "historia", "bom": False},
                {"texto": "faz aí", "bom": False},
            ]},
            {"nome": "Tema", "icone": "💡", "opcoes": [
                {"texto": "sobre um dinossauro gentil", "bom": True},
                {"texto": "sobre impostos", "bom": False},
                {"texto": "sobre nada", "bom": False},
            ]},
            {"nome": "Restrição", "icone": "🚧", "opcoes": [
                {"texto": "de no máximo 8 linhas", "bom": True},
                {"texto": "com 5000 palavras", "bom": False},
                {"texto": "infinita", "bom": False},
            ]},
            {"nome": "Tom", "icone": "🎭", "opcoes": [
                {"texto": "com tom carinhoso", "bom": True},
                {"texto": "assustador", "bom": False},
                {"texto": "muito sério", "bom": False},
            ]},
        ],
    },
    {
        "id": 3,
        "cenario": "Você precisa de ideias para uma feira de ciências do 8º ano.",
        "categorias": [
            {"nome": "Objetivo", "icone": "🎯", "opcoes": [
                {"texto": "Sugira 5 ideias de projetos", "bom": True},
                {"texto": "ideias", "bom": False},
                {"texto": "ajuda", "bom": False},
            ]},
            {"nome": "Contexto", "icone": "🧩", "opcoes": [
                {"texto": "para uma feira de ciências do 8º ano", "bom": True},
                {"texto": "para a faculdade", "bom": False},
                {"texto": "sem contexto", "bom": False},
            ]},
            {"nome": "Restrição", "icone": "🚧", "opcoes": [
                {"texto": "usando materiais baratos", "bom": True},
                {"texto": "usando ouro e diamante", "bom": False},
                {"texto": "sem limites de custo", "bom": False},
            ]},
            {"nome": "Formato", "icone": "📋", "opcoes": [
                {"texto": "com uma frase explicando cada uma", "bom": True},
                {"texto": "tudo em uma palavra", "bom": False},
                {"texto": "sem explicação", "bom": False},
            ]},
        ],
    },
    {
        "id": 4,
        "cenario": "Você quer praticar inglês básico com a ajuda da IA.",
        "categorias": [
            {"nome": "Objetivo", "icone": "🎯", "opcoes": [
                {"texto": "Faça 5 perguntas simples em inglês", "bom": True},
                {"texto": "ingles", "bom": False},
                {"texto": "ensina", "bom": False},
            ]},
            {"nome": "Nível", "icone": "📊", "opcoes": [
                {"texto": "no nível básico", "bom": True},
                {"texto": "no nível avançado", "bom": False},
                {"texto": "muito difícil", "bom": False},
            ]},
            {"nome": "Formato", "icone": "📋", "opcoes": [
                {"texto": "uma pergunta de cada vez", "bom": True},
                {"texto": "todas juntas e embaralhadas", "bom": False},
                {"texto": "sem ordem", "bom": False},
            ]},
            {"nome": "Restrição", "icone": "🚧", "opcoes": [
                {"texto": "corrigindo meus erros em português", "bom": True},
                {"texto": "sem nunca corrigir", "bom": False},
                {"texto": "só em japonês", "bom": False},
            ]},
        ],
    },
    {
        "id": 5,
        "cenario": "Você quer um resumo confiável sobre a Segunda Guerra Mundial.",
        "categorias": [
            {"nome": "Objetivo", "icone": "🎯", "opcoes": [
                {"texto": "Resuma as principais causas", "bom": True},
                {"texto": "guerra", "bom": False},
                {"texto": "conta tudo", "bom": False},
            ]},
            {"nome": "Formato", "icone": "📋", "opcoes": [
                {"texto": "em 4 tópicos", "bom": True},
                {"texto": "em um texto gigante", "bom": False},
                {"texto": "sem formato", "bom": False},
            ]},
            {"nome": "Público", "icone": "👤", "opcoes": [
                {"texto": "para um estudante do 9º ano", "bom": True},
                {"texto": "para um historiador especialista", "bom": False},
                {"texto": "para ninguém", "bom": False},
            ]},
            {"nome": "Senso crítico", "icone": "🧠", "opcoes": [
                {"texto": "e lembre que devo conferir em fontes confiáveis", "bom": True},
                {"texto": "e diga que é a verdade absoluta", "bom": False},
                {"texto": "e não precisa conferir nada", "bom": False},
            ]},
        ],
    },
]
