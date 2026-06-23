"""Testes do GameService (jogo de missões com dificuldade, XP e estrelas)."""

import pytest

from app.services.game_service import GameService

game = GameService()
DIFICULDADES = ("facil", "medio", "dificil")


def test_existem_seis_missoes():
    assert game.total_missions() == 6


def test_cinco_questoes_por_missao():
    assert game.questoes_por_missao == 5


def test_xp_maximo_2000_e_estrelas_18():
    assert game.max_xp() == 2000
    assert game.max_estrelas() == 18


def test_cada_missao_tem_acervo_de_20_questoes():
    for m in game.get_missions():
        assert len(m["questoes"]) == 20


def test_estrutura_das_questoes():
    for m in game.get_missions():
        for q in m["questoes"]:
            assert len(q["alternativas"]) == 3
            assert 0 <= q["correta"] < 3
            assert q["explicacao"]
            assert q["dificuldade"] in DIFICULDADES


def test_cada_missao_tem_pelo_menos_5_de_cada_dificuldade():
    # Garante que dá para sortear 5 questões de qualquer dificuldade.
    for m in game.get_missions():
        for dif in DIFICULDADES:
            qtd = sum(1 for q in m["questoes"] if q["dificuldade"] == dif)
            assert qtd >= 5, f"Missão {m['id']} tem só {qtd} questões '{dif}'"


def test_select_questions_retorna_cinco_da_dificuldade():
    for dif in DIFICULDADES:
        questoes = game.select_questions(1, dif)
        assert len(questoes) == 5
        assert all(q["dificuldade"] == dif for q in questoes)


def test_select_questions_dificuldade_invalida():
    with pytest.raises(ValueError):
        game.select_questions(1, "impossivel")


def test_build_game_monta_seis_missoes_com_cinco_questoes():
    partida = game.build_game("medio")
    assert len(partida) == 6
    assert all(len(m["questoes"]) == 5 for m in partida)


def test_stars_for_correct():
    assert game.stars_for_correct(5) == 3
    assert game.stars_for_correct(4) == 2
    assert game.stars_for_correct(3) == 2
    assert game.stars_for_correct(2) == 1
    assert game.stars_for_correct(1) == 1
    assert game.stars_for_correct(0) == 0


def test_compute_result_perfeito():
    result = game.compute_result([5, 5, 5, 5, 5, 5], "dificil")
    assert result["xp"] == 2000
    assert result["estrelas"] == 18
    assert result["percent"] == 100
    assert result["passou"] is True
    assert result["acertos"] == 30


def test_compute_result_zero():
    result = game.compute_result([0, 0, 0, 0, 0, 0])
    assert result["xp"] == 0
    assert result["estrelas"] == 0
    assert result["passou"] is False


def test_compute_result_xp_cresce_por_missao():
    # 1 acerto na missão 1 vale menos que 1 acerto na missão 6.
    xp_m1 = game.compute_result([1, 0, 0, 0, 0, 0])["xp"]
    xp_m6 = game.compute_result([0, 0, 0, 0, 0, 1])["xp"]
    assert xp_m1 == 40
    assert xp_m6 == 100
    assert xp_m6 > xp_m1


def test_compute_result_limita_acertos():
    # Mais acertos que o número de questões é limitado.
    result = game.compute_result([99, 99, 99, 99, 99, 99])
    assert result["acertos"] == 30
    assert result["xp"] == 2000


def test_meta_minima_500():
    assert game.xp_minimo_meta == 500
    # Exatamente na meta deve passar.
    # Missões 1-5 com 1 acerto cada = 40+50+60+70+80 = 300; + missão 6: 2 acertos = 200 -> 500
    result = game.compute_result([1, 1, 1, 1, 1, 2])
    assert result["xp"] == 500
    assert result["passou"] is True
