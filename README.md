# 🤖 Aprendi.AI

> Aprenda Inteligência Artificial brincando, explorando e criando bons prompts.

**Aprendi.AI** é uma aplicação web educativa, responsiva e *mobile first*, criada para ensinar
Inteligência Artificial a **crianças e adolescentes de 10 a 17 anos**. O conteúdo é apresentado de
forma simples, interativa e gamificada, com trilha de aprendizado, jogo de missões, quiz e
laboratório de prompts.

Este é um **projeto de extensão universitária**, que conecta o conteúdo da disciplina
*Inteligência Artificial para Devs* a uma ação de impacto social.

---

## 🎯 Objetivo

Aproximar a Inteligência Artificial da realidade dos jovens, ensinando:

- O que é IA e como ela funciona (sem complicação);
- A história da IA, de Alan Turing à IA generativa;
- Onde a IA já está no dia a dia;
- Como escrever bons *prompts*;
- Ética, privacidade, segurança e pensamento crítico.

Tudo isso de forma **segura** (sem login e sem coleta de dados pessoais) e **divertida**
(com XP, missões, badges e quizzes).

---

## 🛠️ Tecnologias

| Camada        | Tecnologia                          |
|---------------|-------------------------------------|
| Backend       | Python 3.10+, FastAPI               |
| Templates     | Jinja2                              |
| Frontend      | HTML5, Tailwind CSS (CDN), JavaScript puro |
| Persistência  | Arquivos JSON (sem banco de dados)  |
| Testes        | pytest                              |

O código segue boas práticas de **Clean Code** e **separação em camadas**
(rotas → serviços → dados → armazenamento).

---

## 📦 Instalação

Pré-requisito: **Python 3.10 ou superior**.

```bash
# 1. Clone o repositório
git clone https://github.com/GuilhermeAdias/Aprendi.AI.git
cd Aprendi.AI

# 2. (Recomendado) Crie um ambiente virtual
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt
```

---

## ▶️ Execução

```bash
uvicorn app.main:app --reload
```

Depois abra o navegador em: **http://127.0.0.1:8000**

> Os arquivos de dados (`data/*.json`) são criados automaticamente na primeira execução.

---

## 🧪 Testes

```bash
pytest
```

Os testes cobrem os serviços principais: análise de prompts, quiz, jogo e estatísticas.

---

## 🗺️ Rotas

| Rota                  | Descrição                                                |
|-----------------------|----------------------------------------------------------|
| `/`                   | Página inicial com os cards de navegação                 |
| `/historia`           | Linha do tempo da história da IA                         |
| `/como-funciona`      | Explicação simples de como a IA funciona                 |
| `/dia-a-dia`          | Exemplos de IA no cotidiano                              |
| `/prompts`            | Guia de criação de prompts (com exemplos antes/depois)   |
| `/laboratorio`        | Laboratório de prompts (análise com nota e dicas)        |
| `/jogo`               | Jogo dos Prompts (6 missões, XP e badges)                |
| `/quiz`               | Quiz educativo (10 perguntas)                            |
| `/seguranca`          | Segurança, ética e uso responsável                       |
| `/sobre`              | Sobre o projeto                                          |
| `/avaliacao`          | Questionário de satisfação (salvo em JSON)               |
| `/admin/resultados`   | Painel com os resultados consolidados                    |
| `/health`             | Verificação de saúde da aplicação (JSON)                 |

### Endpoints de API (JSON)

| Método | Rota                    | Descrição                              |
|--------|-------------------------|----------------------------------------|
| POST   | `/laboratorio/analisar` | Analisa um prompt e retorna a avaliação |
| POST   | `/jogo/resultado`       | Salva o resultado de uma partida        |
| POST   | `/quiz/resultado`       | Salva o resultado de um quiz            |

---

## 📁 Estrutura do projeto

```text
Aprendi.AI/
├── app/
│   ├── main.py                 # Cria a aplicação FastAPI e registra as rotas
│   ├── core/
│   │   └── templates.py        # Configuração do Jinja2 e itens de navegação
│   ├── routers/                # Camada de rotas (controllers)
│   │   ├── pages.py
│   │   ├── prompt_lab.py
│   │   ├── game.py
│   │   ├── quiz.py
│   │   ├── evaluation.py
│   │   └── admin.py
│   ├── services/               # Regras de negócio
│   │   ├── prompt_analyzer.py
│   │   ├── game_service.py
│   │   ├── quiz_service.py
│   │   └── statistics_service.py
│   ├── data/                   # Conteúdo educativo estático
│   │   ├── timeline.py
│   │   ├── prompt_examples.py
│   │   ├── ai_examples.py
│   │   ├── missions.py
│   │   └── quiz_questions.py
│   ├── storage/
│   │   └── json_storage.py     # Leitura/escrita dos arquivos JSON
│   ├── templates/              # Páginas Jinja2
│   └── static/                 # CSS e JavaScript
│       ├── css/
│       └── js/
├── data/                       # Persistência (criada/atualizada em runtime)
│   ├── evaluations.json
│   ├── game_scores.json
│   └── quiz_scores.json
├── docs/
│   ├── extensao.md
│   └── evidencias.md
├── tests/
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## 🎓 Como apresentar na extensão

1. **Abertura (5 min):** explique o problema — jovens usam IA, mas nem sempre entendem ou usam com segurança.
2. **Demonstração guiada (15 min):** navegue pela trilha — História → Como funciona → IA no dia a dia → Guia de Prompts.
3. **Mão na massa (15 min):** deixe os participantes usarem o **Laboratório de Prompts**, o **Jogo** e o **Quiz**.
4. **Conversa sobre segurança (5 min):** use a página `/seguranca` e os "Combinados para usar IA do jeito certo".
5. **Avaliação (5 min):** peça que respondam o questionário em `/avaliacao`.
6. **Resultados:** mostre o painel `/admin/resultados` com as médias e comentários.

> Dica: rode em um notebook conectado a um projetor e deixe os celulares dos alunos acessarem
> a mesma rede para usarem a aplicação ao mesmo tempo (o layout é *mobile first*).

---

## 🧾 Evidências necessárias

Veja o checklist completo em [`docs/evidencias.md`](docs/evidencias.md). Em resumo:

- Registro da conversa com a instituição parceira;
- Prints da aplicação (desktop e mobile);
- Foto/registro da apresentação;
- Questionário aplicado e resultados (painel `/admin/resultados`);
- Link deste repositório no GitHub.

---

## 🔒 Privacidade e segurança

- **Sem login** e **sem coleta de dados pessoais**.
- A avaliação é **anônima** (apenas notas de 1 a 5 e um comentário opcional).
- A área `/admin/resultados` **não possui autenticação** (escopo acadêmico). Em produção,
  ela deve ser protegida.

---

## 📜 Licença

Projeto acadêmico de extensão universitária. Uso educacional.
