# Evidências da Atividade Extensionista — Aprendi.AI

As evidências comprovam a execução do projeto. Organize os arquivos em uma pasta
`evidencias/` e nomeie conforme a tabela abaixo.

| # | Evidência | Arquivo sugerido | Descrição |
|---|-----------|------------------|-----------|
| 1 | Conversa com a instituição parceira | `evidencia_01_conversa_instituicao.png` | Registro da conversa inicial com o responsável, mostrando o levantamento de necessidades e a autorização. |
| 2 | Planejamento da aplicação | `evidencia_02_planejamento_aplicacao.pdf` | Documento/imagem com o planejamento de telas, conteúdos e funcionalidades. |
| 3 | Prints da aplicação web | `evidencia_03_prints_aprendiai.png` | Capturas da página inicial, trilha, jogo de prompts, quiz e segurança. |
| 4 | Registro da apresentação | `evidencia_04_apresentacao.jpg` | Foto/captura da apresentação com os alunos, mostrando a interação. |
| 5 | Questionário de avaliação | `evidencia_05_questionario_avaliacao.pdf` | Formulário aplicado aos participantes. |
| 6 | Resultado da avaliação | `evidencia_06_resultados_formulario.pdf` | Consolidação das respostas (exporte o painel `/admin/resultados`). |
| 7 | Repositório no GitHub | (link) | https://github.com/GuilhermeAdias/Aprendi.AI |

---

## Como gerar as evidências da própria aplicação

### Prints (desktop e mobile)

1. Rode a aplicação: `uvicorn app.main:app --reload`.
2. Acesse `http://127.0.0.1:8000`.
3. Capture as telas principais:
   - Página inicial (`/`)
   - História da IA (`/historia`)
   - Laboratório de Prompts com um resultado (`/laboratorio`)
   - Jogo dos Prompts em andamento e a tela final (`/jogo`)
   - Quiz e o resultado final (`/quiz`)
   - Segurança (`/seguranca`)
4. Para o **mobile**, abra as ferramentas de desenvolvedor do navegador (F12) e ative o modo
   dispositivo (Ctrl+Shift+M no Chrome), escolhendo um celular.

### Resultados consolidados

- Após a apresentação, acesse `http://127.0.0.1:8000/admin/resultados`.
- O painel mostra: total de avaliações, média de cada pergunta, total de quizzes e partidas,
  médias de aproveitamento e os comentários.
- Capture a tela ou exporte como PDF (imprimir → salvar como PDF).

### Dados brutos

As respostas ficam salvas em:

- `data/evaluations.json` — avaliações
- `data/quiz_scores.json` — resultados do quiz
- `data/game_scores.json` — resultados do jogo

---

## Checklist de evidências

- [ ] Registro da conversa com a instituição parceira
- [ ] Planejamento da aplicação
- [ ] Prints da aplicação (desktop)
- [ ] Prints da aplicação (mobile)
- [ ] Foto/registro da apresentação
- [ ] Questionário aplicado
- [ ] Resultados consolidados (`/admin/resultados`)
- [ ] Link do repositório no GitHub
