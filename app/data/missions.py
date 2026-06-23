"""Missões do Jogo dos Prompts.

Cada missão apresenta um objetivo e três opções de prompt. O jogador deve
escolher o melhor prompt. A resposta correta vem acompanhada de uma
explicação educativa.
"""

from __future__ import annotations

# XP concedido por missão acertada.
XP_POR_ACERTO = 100

MISSIONS: list[dict] = [
    {
        "id": 1,
        "titulo": "Missão 1 — A lição de casa de Ciências",
        "descricao": (
            "Você precisa de ajuda para entender o ciclo da água para uma "
            "prova. Qual prompt traz a melhor explicação?"
        ),
        "prompts": [
            "água",
            "fala do ciclo da agua",
            (
                "Explique o ciclo da água de forma simples para um estudante "
                "de 11 anos, em 4 passos e com um exemplo do dia a dia."
            ),
        ],
        "correta": 2,
        "explicacao": (
            "O melhor prompt tem objetivo (explicar), público (11 anos), "
            "formato (4 passos) e ainda pede um exemplo. Quanto mais claro, "
            "melhor a resposta da IA!"
        ),
    },
    {
        "id": 2,
        "titulo": "Missão 2 — Uma história para dormir",
        "descricao": (
            "Você quer criar uma historinha para o seu irmão mais novo. Qual "
            "prompt funciona melhor?"
        ),
        "prompts": [
            (
                "Crie uma história curta e calma, de até 8 linhas, sobre uma "
                "estrela que tem medo do escuro. O público é uma criança de 6 "
                "anos, com tom carinhoso."
            ),
            "historia",
            "faz uma historia ai",
        ],
        "correta": 0,
        "explicacao": (
            "Esse prompt define objetivo (história), restrição (8 linhas), "
            "tema (estrela com medo do escuro), público (6 anos) e tom "
            "(carinhoso). Tudo o que a IA precisa para acertar!"
        ),
    },
    {
        "id": 3,
        "titulo": "Missão 3 — Resumo do livro",
        "descricao": (
            "Você leu um capítulo e quer um resumo para revisar. Qual prompt "
            "é o mais completo?"
        ),
        "prompts": [
            "resume",
            (
                "Resuma o texto abaixo em 5 tópicos curtos, destacando as "
                "ideias mais importantes, com linguagem simples. Texto: [colar "
                "o texto aqui]."
            ),
            "faz um resumo grande",
        ],
        "correta": 1,
        "explicacao": (
            "O prompt vencedor diz o formato (5 tópicos), o objetivo (resumir "
            "as ideias importantes), o tom (simples) e ainda mostra onde "
            "colar o texto. Dar o material ajuda muito a IA."
        ),
    },
    {
        "id": 4,
        "titulo": "Missão 4 — Treino de inglês",
        "descricao": (
            "Você quer praticar inglês com a IA. Qual prompt deixa o treino "
            "mais útil?"
        ),
        "prompts": [
            "ensina ingles",
            "ingles",
            (
                "Quero praticar inglês básico. Faça 5 perguntas simples em "
                "inglês, uma de cada vez, e corrija meus erros explicando em "
                "português."
            ),
        ],
        "correta": 2,
        "explicacao": (
            "Esse prompt define objetivo (praticar), formato (5 perguntas, "
            "uma de cada vez), nível (básico) e restrição (correção em "
            "português). Assim o treino fica organizado."
        ),
    },
    {
        "id": 5,
        "titulo": "Missão 5 — Ideias para um projeto",
        "descricao": (
            "Você precisa de ideias para uma feira de ciências. Qual prompt "
            "traz ideias mais úteis?"
        ),
        "prompts": [
            (
                "Sugira 5 ideias de projetos simples para uma feira de "
                "ciências do 8º ano, usando materiais baratos. Para cada "
                "ideia, escreva uma frase explicando o que ela demonstra."
            ),
            "ideias",
            "me da umas ideias de projeto",
        ],
        "correta": 0,
        "explicacao": (
            "O melhor prompt tem objetivo (5 ideias), contexto (feira do 8º "
            "ano), restrição (materiais baratos) e formato (uma explicação "
            "por ideia). Quanto mais detalhe, melhores as ideias."
        ),
    },
    {
        "id": 6,
        "titulo": "Missão 6 — Cuidado com a informação",
        "descricao": (
            "A IA pode errar. Qual prompt mostra que você usa a IA com "
            "pensamento crítico?"
        ),
        "prompts": [
            "me fala a verdade absoluta sobre tudo",
            (
                "Explique as principais causas da Segunda Guerra Mundial em 4 "
                "tópicos e, no final, indique que eu devo confirmar as "
                "informações em fontes confiáveis."
            ),
            "responde rapido sem pensar",
        ],
        "correta": 1,
        "explicacao": (
            "O prompt vencedor pede uma resposta organizada (4 tópicos) e "
            "lembra de verificar as informações. Usar a IA com senso crítico "
            "é uma das atitudes mais importantes!"
        ),
    },
]
