"""Testes do QuizService."""

from app.services.quiz_service import QuizService

quiz = QuizService()


def test_existem_dez_perguntas():
    assert quiz.total_questions() == 10


def test_cada_pergunta_tem_estrutura_valida():
    for q in quiz.get_questions():
        assert "pergunta" in q
        assert len(q["alternativas"]) == 4
        assert 0 <= q["correta"] < 4
        assert q["explicacao"]


def test_compute_score_todos_certos():
    result = quiz.compute_score(10)
    assert result["correct"] == 10
    assert result["percent"] == 100
    assert result["xp"] == 10 * quiz.xp_por_acerto


def test_compute_score_metade():
    result = quiz.compute_score(5)
    assert result["correct"] == 5
    assert result["percent"] == 50


def test_compute_score_limita_valores():
    assert quiz.compute_score(999)["correct"] == 10
    assert quiz.compute_score(-5)["correct"] == 0


def test_score_answers_corrige_corretamente():
    # Responde todas certas usando o gabarito.
    respostas = {q["id"]: q["correta"] for q in quiz.get_questions()}
    result = quiz.score_answers(respostas)
    assert result["correct"] == 10
    assert result["percent"] == 100
    assert "details" in result
    assert all(d["is_correct"] for d in result["details"])


def test_score_answers_com_erros():
    # Responde todas erradas (escolhe um índice diferente do correto).
    respostas = {
        q["id"]: (q["correta"] + 1) % 4 for q in quiz.get_questions()
    }
    result = quiz.score_answers(respostas)
    assert result["correct"] == 0
    assert result["percent"] == 0
