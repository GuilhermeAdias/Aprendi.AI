"""Testes do GameService."""

from app.services.game_service import GameService

game = GameService()


def test_existem_seis_missoes():
    assert game.total_missions() == 6


def test_cada_missao_tem_estrutura_valida():
    for m in game.get_missions():
        assert "titulo" in m
        assert "descricao" in m
        assert len(m["prompts"]) == 3
        assert 0 <= m["correta"] < 3
        assert m["explicacao"]


def test_max_xp():
    assert game.max_xp() == 6 * game.xp_por_acerto


def test_compute_score_todos_certos():
    result = game.compute_score(6)
    assert result["correct"] == 6
    assert result["percent"] == 100
    assert result["xp"] == game.max_xp()


def test_compute_score_limita_valores():
    assert game.compute_score(100)["correct"] == 6
    assert game.compute_score(-3)["correct"] == 0


def test_evaluate_answer_correta():
    missao = game.get_missions()[0]
    result = game.evaluate_answer(missao["id"], missao["correta"])
    assert result["correct"] is True
    assert result["xp"] == game.xp_por_acerto


def test_evaluate_answer_errada():
    missao = game.get_missions()[0]
    indice_errado = (missao["correta"] + 1) % 3
    result = game.evaluate_answer(missao["id"], indice_errado)
    assert result["correct"] is False
    assert result["xp"] == 0


def test_evaluate_answer_missao_inexistente():
    import pytest

    with pytest.raises(ValueError):
        game.evaluate_answer(9999, 0)
