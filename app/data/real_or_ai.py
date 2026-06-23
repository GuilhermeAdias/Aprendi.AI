"""Dados do game 'Real ou IA?'.

O jogador lê uma situação e adivinha se aquilo foi (provavelmente) feito por um
ser humano ou gerado por Inteligência Artificial. O objetivo é treinar o
pensamento crítico e a percepção sobre conteúdo gerado por IA.

Cada item tem:
- ``conteudo``: a descrição da situação;
- ``resposta``: "ia" ou "humano";
- ``explicacao``: por que;
- ``dica``: um sinal que ajuda a perceber.
"""

from __future__ import annotations

XP_POR_ACERTO = 30

ITENS: list[dict] = [
    {
        "conteudo": "Um texto perfeito de 3 parágrafos sobre QUALQUER tema, escrito em 2 segundos.",
        "resposta": "ia",
        "explicacao": "Escrever bem sobre qualquer assunto instantaneamente é típico de uma IA.",
        "dica": "Velocidade sobre-humana e 'saber de tudo' são sinais de IA.",
    },
    {
        "conteudo": "Um bilhete escrito à mão, com a letra um pouco torta e um erro rabiscado.",
        "resposta": "humano",
        "explicacao": "Letra torta, rasuras e imperfeições são bem humanas.",
        "dica": "Imperfeições e marcas pessoais geralmente indicam um humano.",
    },
    {
        "conteudo": "Uma imagem de uma pessoa sorrindo, mas com 6 dedos em uma das mãos.",
        "resposta": "ia",
        "explicacao": "Erros estranhos como dedos a mais são comuns em imagens de IA.",
        "dica": "Mãos, dentes e textos errados costumam denunciar imagens de IA.",
    },
    {
        "conteudo": "Um desenho de criança com giz de cera, fora das linhas e cheio de cor.",
        "resposta": "humano",
        "explicacao": "O jeitinho imperfeito e espontâneo é muito humano.",
        "dica": "Espontaneidade e 'fora das linhas' são marcas humanas.",
    },
    {
        "conteudo": "Uma resposta que muda totalmente de assunto e inventa um fato que não existe.",
        "resposta": "ia",
        "explicacao": "Inventar fatos (alucinar) é um erro conhecido das IAs.",
        "dica": "Quando algo parece inventado com confiança, pode ser IA.",
    },
    {
        "conteudo": "Uma redação com uma história pessoal real sobre o cachorro de estimação.",
        "resposta": "humano",
        "explicacao": "Memórias e sentimentos pessoais reais vêm de pessoas.",
        "dica": "Experiências e emoções verdadeiras indicam um humano.",
    },
    {
        "conteudo": "Uma 'foto' de um gato astronauta tocando violão na Lua, super realista.",
        "resposta": "ia",
        "explicacao": "Cenas impossíveis e realistas ao mesmo tempo são geradas por IA.",
        "dica": "Se a cena é impossível mas parece foto, provavelmente é IA.",
    },
    {
        "conteudo": "Um comentário com erro de digitação e uma piada interna com os amigos.",
        "resposta": "humano",
        "explicacao": "Erros de digitação e piadas internas são bem humanos.",
        "dica": "Gírias, piadas internas e erros casuais sugerem humano.",
    },
    {
        "conteudo": "Um texto que repete a mesma estrutura perfeita em todas as frases, sem nenhum erro.",
        "resposta": "ia",
        "explicacao": "Perfeição e padrão muito regular podem indicar texto de IA.",
        "dica": "Texto 'perfeito demais' e padronizado pode ser de IA.",
    },
    {
        "conteudo": "Uma carta com a letra do seu avô e o cheiro do papel guardado há anos.",
        "resposta": "humano",
        "explicacao": "Objetos físicos com história pessoal são de pessoas reais.",
        "dica": "Coisas do mundo físico com história pessoal são humanas.",
    },
    {
        "conteudo": "Uma música nova 'no estilo' de um artista famoso, criada em segundos a pedido.",
        "resposta": "ia",
        "explicacao": "Gerar música imitando um estilo na hora é tarefa de IA.",
        "dica": "Criar 'no estilo de' instantaneamente é sinal de IA.",
    },
    {
        "conteudo": "Um diário com sentimentos confusos, medos e sonhos sobre o futuro.",
        "resposta": "humano",
        "explicacao": "Sentimentos íntimos e contraditórios são profundamente humanos.",
        "dica": "Emoções íntimas e dúvidas reais indicam um humano.",
    },
]
