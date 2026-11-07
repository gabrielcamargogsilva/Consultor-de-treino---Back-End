from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from services import busca_semantica, processamento_texto


def test_carrega_documentos_e_define_categoria_por_pasta(tmp_path, monkeypatch):
    documento = SimpleNamespace(
        metadata={"source": str(tmp_path / "forca" / "guia.pdf")}
    )
    loader = Mock()
    loader.load.return_value = [documento]
    monkeypatch.setattr(
        processamento_texto, "DirectoryLoader", Mock(return_value=loader)
    )

    splitter = Mock()
    splitter.split_documents.return_value = ["trecho"]
    monkeypatch.setattr(
        processamento_texto,
        "RecursiveCharacterTextSplitter",
        Mock(return_value=splitter),
    )

    resultado = processamento_texto.carregar_e_dividir_textos(str(tmp_path))

    assert documento.metadata["categoria"] == "forca"
    assert resultado == ["trecho"]
    splitter.split_documents.assert_called_once_with([documento])


def test_falha_quando_nao_encontra_documentos(monkeypatch, tmp_path):
    loader = Mock()
    loader.load.return_value = []
    monkeypatch.setattr(
        processamento_texto, "DirectoryLoader", Mock(return_value=loader)
    )

    with pytest.raises(
        FileNotFoundError,
        match="Nenhum documento PDF encontrado",
    ):
        processamento_texto.carregar_e_dividir_textos(str(tmp_path))


def test_busca_contexto_aplica_categoria_e_junta_resultados(monkeypatch):
    embeddings = object()
    vectorstore = Mock()
    vectorstore.similarity_search.return_value = [
        SimpleNamespace(page_content="Primeiro trecho"),
        SimpleNamespace(page_content="Segundo trecho"),
    ]
    chroma = Mock(return_value=vectorstore)
    monkeypatch.setattr(
        busca_semantica,
        "obter_modelo_embeddings",
        lambda: embeddings,
    )
    monkeypatch.setattr(busca_semantica, "Chroma", chroma)

    resultado = busca_semantica.buscar_contexto_exercicios(
        query="agachamento",
        diretorio_banco="banco",
        categoria="hipertrofia",
        top_k=2,
    )

    assert resultado == "Primeiro trecho\n\n---\n\nSegundo trecho"
    chroma.assert_called_once_with(
        persist_directory="banco",
        embedding_function=embeddings,
    )
    vectorstore.similarity_search.assert_called_once_with(
        "agachamento",
        k=2,
        filter={"categoria": "hipertrofia"},
    )


def test_busca_sem_categoria_nao_aplica_filtro(monkeypatch):
    vectorstore = Mock()
    vectorstore.similarity_search.return_value = []
    monkeypatch.setattr(
        busca_semantica,
        "obter_modelo_embeddings",
        lambda: object(),
    )
    monkeypatch.setattr(
        busca_semantica,
        "Chroma",
        Mock(return_value=vectorstore),
    )

    resultado = busca_semantica.buscar_contexto_exercicios(
        query="agachamento",
        diretorio_banco="banco",
    )

    assert resultado == ""
    vectorstore.similarity_search.assert_called_once_with(
        "agachamento",
        k=3,
        filter=None,
    )
