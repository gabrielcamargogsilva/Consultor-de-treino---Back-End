
from app import buscar_exercicios


def test_retorna_exercicios_do_grupo_cadastrado():
    resultado = buscar_exercicios("costas")

    assert resultado == [
        "Puxada frontal",
        "Remada baixa",
        "Remada unilateral",
    ]


def test_normaliza_grupo_muscular():
    resultado = buscar_exercicios("  COSTAS  ")

    assert resultado == [
        "Puxada frontal",
        "Remada baixa",
        "Remada unilateral",
    ]


def test_retorna_lista_vazia_para_grupo_desconhecido():
    resultado = buscar_exercicios("ombros")

    assert resultado == []
