from langchain_google_genai import GoogleGenerativeAIEmbeddings


def obter_modelo_embeddings():
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001")
