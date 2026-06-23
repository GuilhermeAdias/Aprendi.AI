"""Testes do PromptAnalyzerService."""

from app.services.prompt_analyzer import PromptAnalyzerService

analyzer = PromptAnalyzerService()


def test_prompt_vazio_recebe_nota_zero():
    result = analyzer.analyze("")
    assert result["score"] == 0
    assert result["level"] == "Vazio"
    assert result["improvements"]


def test_prompt_completo_recebe_nota_alta():
    prompt = (
        "Explique para um aluno de 11 anos o que é fotossíntese, em 4 tópicos "
        "simples e de forma divertida, considerando que sou estudante."
    )
    result = analyzer.analyze(prompt)
    assert result["score"] >= 70
    assert result["level"] in ("Avançado", "Mestre dos Prompts")
    assert len(result["strengths"]) >= 3


def test_prompt_fraco_recebe_nota_baixa_e_sugestoes():
    result = analyzer.analyze("planetas")
    assert result["score"] < 50
    assert len(result["improvements"]) >= 1


def test_estrutura_do_retorno():
    result = analyzer.analyze("Crie uma lista de dicas de estudo")
    for chave in ("score", "level", "strengths", "improvements", "suggested_prompt"):
        assert chave in result
    assert 0 <= result["score"] <= 100
    assert isinstance(result["strengths"], list)
    assert isinstance(result["improvements"], list)
    assert isinstance(result["suggested_prompt"], str)


def test_score_sempre_entre_0_e_100():
    prompts = [
        "",
        "oi",
        "VC PODE ME AJUDAR PQ TD",
        "Explique, em uma tabela, para um aluno de 10 anos, de forma simples, "
        "o que é IA, considerando que sou estudante e preciso para a prova.",
    ]
    for p in prompts:
        result = analyzer.analyze(p)
        assert 0 <= result["score"] <= 100


def test_sugestao_nao_vazia_para_prompt_fraco():
    result = analyzer.analyze("historia")
    assert result["suggested_prompt"].strip() != ""
