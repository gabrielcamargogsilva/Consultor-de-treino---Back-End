from pathlib import Path

from langchain_chroma import Chroma
from services.geracao_embeddings import obter_modelo_embeddings


def buscar_contexto_exercicios(
    query: str,
    diretorio_banco: str,
    categoria: str | None = None,
    top_k: int = 3,
):
    embeddings = obter_modelo_embeddings()
    vectorstore = Chroma(
        persist_directory=diretorio_banco,
        embedding_function=embeddings,
    )

    filtro = {"categoria": categoria} if categoria else None
    resultados = vectorstore.similarity_search(query, k=top_k, filter=filtro)

    textos_recuperados = [doc.page_content for doc in resultados]
    return "\n\n---\n\n".join(textos_recuperados)


if __name__ == "__main__":
    raiz_projeto = Path(__file__).resolve().parents[1]
    contexto = buscar_contexto_exercicios(
        query="Qual a postura correta para o agachamento livre?",
        diretorio_banco=str(raiz_projeto / "chroma_db_treinai"),
        categoria="hipertrofia",
    )
    print(contexto)
