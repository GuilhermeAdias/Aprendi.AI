"""Perguntas do Quiz educativo sobre Inteligência Artificial.

10 perguntas, cada uma com 4 alternativas, índice da correta e explicação.
"""

from __future__ import annotations

# XP por resposta correta no quiz.
XP_POR_ACERTO = 50

QUIZ_QUESTIONS: list[dict] = [
    {
        "id": 1,
        "pergunta": "O que é Inteligência Artificial (IA)?",
        "alternativas": [
            "Um robô que sente emoções como os humanos",
            "Programas de computador que aprendem padrões para realizar tarefas",
            "Um tipo de celular novo",
            "Uma pessoa muito inteligente",
        ],
        "correta": 1,
        "explicacao": (
            "IA são programas que aprendem padrões a partir de muitos dados "
            "para realizar tarefas, como recomendar vídeos ou traduzir textos."
        ),
    },
    {
        "id": 2,
        "pergunta": "A IA pode errar?",
        "alternativas": [
            "Não, a IA acerta sempre",
            "Só erra quando está sem internet",
            "Sim, ela pode errar e inventar informações",
            "Nunca, porque ela é um computador",
        ],
        "correta": 2,
        "explicacao": (
            "Sim! A IA pode errar e até inventar informações que parecem "
            "verdadeiras. Por isso devemos sempre conferir o que ela responde."
        ),
    },
    {
        "id": 3,
        "pergunta": "Como a IA aprende?",
        "alternativas": [
            "Estudando em escolas como as crianças",
            "Observando muitos exemplos e encontrando padrões",
            "Lendo a mente das pessoas",
            "Ela já nasce sabendo tudo",
        ],
        "correta": 1,
        "explicacao": (
            "A IA aprende vendo muitos exemplos (dados) e descobrindo padrões "
            "entre eles. Quanto mais bons exemplos, melhor ela fica."
        ),
    },
    {
        "id": 4,
        "pergunta": "O que é um 'prompt'?",
        "alternativas": [
            "Um tipo de vírus de computador",
            "O comando ou pedido que escrevemos para a IA",
            "Um botão de ligar o computador",
            "Um jogo de tabuleiro",
        ],
        "correta": 1,
        "explicacao": (
            "Prompt é o pedido que você escreve para a IA. Quanto mais claro "
            "e detalhado o prompt, melhor costuma ser a resposta."
        ),
    },
    {
        "id": 5,
        "pergunta": "Qual destes é um bom prompt?",
        "alternativas": [
            "futebol",
            "fala de futebol",
            "Explique as regras básicas do futebol em 5 tópicos simples para uma criança de 10 anos",
            "?",
        ],
        "correta": 2,
        "explicacao": (
            "O bom prompt tem objetivo (explicar regras), formato (5 tópicos) "
            "e público (criança de 10 anos). Detalhes ajudam a IA a acertar."
        ),
    },
    {
        "id": 6,
        "pergunta": "Qual destes NÃO é um exemplo de IA no dia a dia?",
        "alternativas": [
            "Recomendações de vídeos no YouTube",
            "Rota mais rápida no Google Maps",
            "Uma cadeira de madeira comum",
            "Corretor automático do celular",
        ],
        "correta": 2,
        "explicacao": (
            "Uma cadeira comum não usa IA. Já as recomendações, mapas e "
            "corretores automáticos usam Inteligência Artificial."
        ),
    },
    {
        "id": 7,
        "pergunta": "Devo compartilhar dados pessoais (endereço, senha) com a IA?",
        "alternativas": [
            "Sim, sempre",
            "Não, devemos proteger nossos dados pessoais",
            "Só se a IA pedir com educação",
            "Só aos domingos",
        ],
        "correta": 1,
        "explicacao": (
            "Nunca compartilhe dados pessoais como endereço, telefone ou "
            "senhas. Proteger sua privacidade é fundamental na internet."
        ),
    },
    {
        "id": 8,
        "pergunta": "Se a IA te der uma informação importante, o que fazer?",
        "alternativas": [
            "Acreditar sem pensar",
            "Verificar em fontes confiáveis",
            "Apagar o computador",
            "Repassar para todo mundo na hora",
        ],
        "correta": 1,
        "explicacao": (
            "Sempre verifique informações importantes em fontes confiáveis. A "
            "IA ajuda, mas o pensamento crítico é seu!"
        ),
    },
    {
        "id": 9,
        "pergunta": "A IA pensa e sente exatamente como um ser humano?",
        "alternativas": [
            "Sim, é igualzinha a uma pessoa",
            "Não, ela calcula padrões e não tem sentimentos de verdade",
            "Sim, ela fica triste quando erra",
            "Sim, ela sonha à noite",
        ],
        "correta": 1,
        "explicacao": (
            "A IA não pensa nem sente como nós. Ela faz cálculos com padrões "
            "que aprendeu. Parece humana, mas não tem sentimentos de verdade."
        ),
    },
    {
        "id": 10,
        "pergunta": "Qual é a melhor forma de usar a IA nos estudos?",
        "alternativas": [
            "Copiar tudo sem entender",
            "Usar como apoio para aprender e tirar dúvidas, sempre pensando junto",
            "Deixar a IA fazer toda a prova por você",
            "Nunca mais estudar",
        ],
        "correta": 1,
        "explicacao": (
            "A IA é uma ferramenta de apoio: ótima para tirar dúvidas e "
            "aprender. Mas o raciocínio e o aprendizado precisam ser seus!"
        ),
    },
]
