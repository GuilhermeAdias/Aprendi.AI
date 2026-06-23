"""Testes do StatisticsService.

Os métodos aceitam listas explícitas, permitindo testar as agregações sem
depender dos arquivos em disco.
"""

from app.services.statistics_service import StatisticsService

stats = StatisticsService()


def _avaliacao(nota: int, comentario: str = ""):
    return {
        "facilidade": nota,
        "entendeu_ia": nota,
        "aprendeu_prompts": nota,
        "jogo_ajudou": nota,
        "entendeu_erro": nota,
        "comentario": comentario,
        "timestamp": "2026-01-01T00:00:00+00:00",
    }


def test_evaluation_stats_vazio():
    result = stats.evaluation_stats([])
    assert result["total"] == 0
    assert result["overall_average"] == 0.0
    assert result["comments"] == []
    assert len(result["averages"]) == 5


def test_evaluation_stats_calcula_medias():
    avaliacoes = [_avaliacao(5), _avaliacao(3)]
    result = stats.evaluation_stats(avaliacoes)
    assert result["total"] == 2
    for media in result["averages"]:
        assert media["average"] == 4.0
    assert result["overall_average"] == 4.0


def test_evaluation_stats_coleta_comentarios():
    avaliacoes = [
        _avaliacao(4, "Muito legal!"),
        _avaliacao(5, "   "),  # comentário vazio deve ser ignorado
        _avaliacao(5, "Aprendi bastante"),
    ]
    result = stats.evaluation_stats(avaliacoes)
    textos = [c["texto"] for c in result["comments"]]
    assert "Muito legal!" in textos
    assert "Aprendi bastante" in textos
    assert len(result["comments"]) == 2


def test_quiz_stats():
    scores = [
        {"correct": 8, "total": 10, "percent": 80, "xp": 400},
        {"correct": 6, "total": 10, "percent": 60, "xp": 300},
    ]
    result = stats.quiz_stats(scores)
    assert result["total"] == 2
    assert result["average_percent"] == 70.0
    assert result["average_correct"] == 7.0


def test_game_stats():
    scores = [
        {"correct": 6, "total": 6, "percent": 100, "xp": 600},
        {"correct": 3, "total": 6, "percent": 50, "xp": 300},
    ]
    result = stats.game_stats(scores)
    assert result["total"] == 2
    assert result["average_percent"] == 75.0
    assert result["average_xp"] == 450.0


def test_game_stats_vazio():
    result = stats.game_stats([])
    assert result["total"] == 0
    assert result["average_percent"] == 0.0
