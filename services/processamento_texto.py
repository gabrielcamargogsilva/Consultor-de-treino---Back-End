from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def carregar_e_dividir_textos(diretorio_raiz: str):
    loader = DirectoryLoader(
        diretorio_raiz,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
    )
    documentos = loader.load()

    if not documentos:
        raise FileNotFoundError(
            f"Nenhum documento PDF encontrado em: {diretorio_raiz}"
        )

    for doc in documentos:
        origem = doc.metadata.get("source")
        if origem:
            doc.metadata["categoria"] = Path(origem).parent.name

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    return text_splitter.split_documents(documentos)
