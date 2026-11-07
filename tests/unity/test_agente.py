from app import buscar_exercicios, client
from google.genai import types


def executar_teste_agente():
    resposta = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=(
            "Monte uma sugestão de treino para costas. "
            "Consulte buscar_exercicios para o grupo muscular "
            "'costas' e use os exercícios retornados. "
            "Não invente resultados da ferramenta."
        ),
        config={
            "tools": [buscar_exercicios],
            "automatic_function_calling": (
                types.AutomaticFunctionCallingConfig(
                    maximum_remote_calls=2
                )
            ),
        },
    )

    if resposta.text is None:
        raise ValueError(
            "O Gemini não retornou uma resposta textual final."
        )

    return resposta.text


if __name__ == "__main__":
    print(executar_teste_agente())
