from pathlib import Path

from langchain_chroma import Chroma
from services.processamento_texto import carregar_e_dividir_textos
from services.geracao_embeddings import obter_modelo_embeddings


def popular_banco_vetorial(diretorio_dados: str, diretorio_banco: str):
    chunks = carregar_e_dividir_textos(diretorio_dados)
    embeddings = obter_modelo_embeddings()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=diretorio_banco,
    )
    return vectorstore


if __name__ == "__main__":
    raiz_projeto = Path(__file__).resolve().parents[1]
    diretorio_dados = raiz_projeto / "data" / "documentos"
    diretorio_banco = raiz_projeto / "chroma_db_treinai"
    popular_banco_vetorial(str(diretorio_dados), str(diretorio_banco))
