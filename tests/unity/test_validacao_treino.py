
import pytest

from app import validar_resposta_treino


def test_aceita_resposta_valida():
    resultado = {
        "plano_markdown": "## Treino de costas",
        "avisos_importantes": ["Respeite seus limites."],
        "sugestoes_adicionais": "Priorize a recuperação.",
    }

    assert validar_resposta_treino(resultado) == resultado


def test_rejeita_campo_obrigatorio_ausente():
    resultado = {
        "plano_markdown": "## Treino de costas",
        "sugestoes_adicionais": "Priorize a recuperação.",
    }

    with pytest.raises(ValueError):
        validar_resposta_treino(resultado)


def test_rejeita_tipo_incorreto():
    resultado = {
        "plano_markdown": "## Treino de costas",
        "avisos_importantes": "Isto deveria ser uma lista",
        "sugestoes_adicionais": "Priorize a recuperação.",
    }

    with pytest.raises(ValueError):
        validar_resposta_treino(resultado)
