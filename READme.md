### Curso Técnico de Desenvolvimento de Sistemas - Senai Itapeva

# API - Consultor de Treinos Personalizados

Esta é a **API REST** responsável por gerar planos de treino personalizados com base nas informações fornecidas pelo usuário. Ela utiliza a **IA generativa da Google (Gemini)** para montar um plano detalhado em Markdown, com sugestões e avisos importantes. A API foi desenvolvida em **Python** com **Flask**, utilizando boas práticas de validação de dados e separação de responsabilidades.

## Status do Projeto
✅ Projeto Finalizado

## Índice
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Aprendizados](#aprendizados)
- [Rotas da API](#rotas-da-api)
- [Como Rodar o Projeto](#como-rodar-o-projeto)
- [Autor](#autor)
- [Licença](#licença)

## Funcionalidades
- Geração de planos de treino personalizados usando IA
- Retorno estruturado em formato JSON:
  - Plano de treino em Markdown
  - Avisos importantes
  - Sugestões adicionais
- Validação de dados da requisição
- Tratamento de erros com mensagens claras
- Suporte a CORS para integração com aplicações front-end

## Tecnologias Utilizadas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Google AI](https://img.shields.io/badge/Google_Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)
![JSON](https://img.shields.io/badge/JSON-000000?style=for-the-badge&logo=json&logoColor=white)
![CORS](https://img.shields.io/badge/CORS-enabled-blue?style=for-the-badge)

## 📚 Aprendizados
Durante o desenvolvimento da API, foram aprofundados conhecimentos em:
- Criação de APIs RESTful com Flask
- Integração com IA generativa da Google via `google.genai`
- Tratamento e validação de requisições JSON
- Organização do código por funções reutilizáveis
- Segurança com variáveis de ambiente via `.env`
- Manipulação de respostas com `jsonify()` e códigos HTTP apropriados

## Acesse o Consultor de Treinos
**Vercel:** [https://consultor-de-treinos.vercel.app](https://consultor-de-treinos.vercel.app) 
**Repositório GitHub:** [https://consultor-de-treino-front-end.vercel.app/](https://consultor-de-treino-front-end.vercel.app/) 

## Rotas da API

### `GET /`
Retorna uma mensagem simples de verificação:  
`"API está funcionando!"`

---

### `POST /gerar_treino`

**Descrição:** Gera um plano de treino personalizado com base nas informações enviadas.

**Corpo da Requisição (JSON):**
```json
{
  "objetivo": "Ganhar massa muscular",
  "nivel": "Iniciante",
  "acesso_equipamentos": "Academia completa",
  "restricoes": "Problema no joelho",
  "especificacao_treino": "Adaptação para jogadores de basquete"
}
```

**Resposta (JSON):**
```json
{
  "plano_markdown": "...conteúdo em markdown...",
  "avisos_importantes": ["Evite treinar com dor", "Hidrate-se durante os treinos"],
  "sugestoes_adicionais": "Durma bem, alimente-se corretamente, respeite os dias de descanso."
}
```

**Códigos de Resposta:**
- `200 OK`: Treino gerado com sucesso
- `400 Bad Request`: Dados incompletos ou inválidos
- `500 Internal Server Error`: Erro interno ao processar o plano

## Como Rodar o Projeto

### Pré-requisitos
- Python 3.10 ou superior
- Conta no [Google AI Studio](https://aistudio.google.com/) com uma chave da API Gemini

### Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio-api.git
   cd seu-repositorio-api
   ```

2. **Crie e ative um ambiente virtual (opcional):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Crie um arquivo `.env` e adicione sua chave da API:**
   ```
   GOOGLE_API_KEY=sua-chave-aqui
   ```

5. **Inicie o servidor:**
   ```bash
   python app.py
   ```

6. A API estará disponível em `http://localhost:5000`.

### Indexar PDFs para busca semântica

Coloque os documentos em `data/documentos/<categoria>/` e configure `GOOGLE_API_KEY` no `.env`. Na raiz do projeto, execute:

```bash
python -m services.ingestao_documentos
```

O banco vetorial será salvo em `chroma_db_treinai/`. Para consultar trechos relevantes pelo código, use `buscar_contexto_exercicios` em `services.busca_semantica`; esse serviço ainda não está conectado a uma rota HTTP.

## Autor
- **Gabriel Camargo Gonçalves Silva**  
  [GitHub](https://github.com/gabrielcamargogsilva)  
  • gabriel.cgsilva.senai@gmail.com  
  • gabrielcamargogsilva@gmail.com

## Licença
Este projeto está licenciado sob a Licença MIT 
