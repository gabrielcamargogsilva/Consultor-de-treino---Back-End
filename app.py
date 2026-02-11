from flask import Flask, jsonify, request, send_file
import json
from flask_cors import CORS
from google import genai
import os
from dotenv import load_dotenv
from fpdf import FPDF
import io



# Carrega variáveis de ambiente do .env
load_dotenv()

app = Flask(__name__)
CORS(app)

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


# Função para criar o plano de treino via Gemini
def criar_treino(objetivo, nivel, acesso_equipamentos, restricoes, especificacao_treino):
    prompt = f"""
        Você é um personal trainer experiente e especialista em criar rotinas de treino personalizadas.
        Com base nas informações do usuário abaixo, crie um plano de treino detalhado. Sua resposta deve ser respeitosa e profissional, evitando o uso de palavras de baixo calão, conteúdo sexual, assédio ou qualquer outro tipo de linguagem imprópria.
        Retorne sua resposta ESTRITAMENTE no seguinte formato JSON. Não adicione nenhum texto antes ou depois do JSON:

        {{
            "plano_markdown": "string_contendo_o_plano_de_treino_formatado_em_markdown",
            "avisos_importantes": [
                "string_aviso_1",
                "string_aviso_2_se_aplicavel"
            ],
            "sugestoes_adicionais": "string_com_sugestoes_gerais_sobre_progressao_nutricao_descanso"
        }}

        Informações do usuário:
        - Objetivo: {objetivo}
        - Nível de Experiência: {nivel}
        - Acesso a Equipamentos: {acesso_equipamentos}
        - Restrições Físicas: {restricoes}
        - Especificação do Treino (caso o usuário queira algo específico, como "adaptação para jogadores de basquete"): {especificacao_treino}

        Instruções para o conteúdo de "plano_markdown":
        1. Deve ser uma string única contendo o plano de treino completo.
        2. Use formatação Markdown (ex: ## Títulos, **negrito**, *itálico*, - Listas).
        3. Inclua distribuição semanal (ex: Segunda, Quarta, Sexta).
        4. Para cada dia de treino: aquecimento, lista de exercícios (com séries, repetições, descanso) e desaquecimento/alongamento.
        5. Adapte os exercícios para as restrições e equipamentos disponíveis.
        6. Considere as especificações adicionais fornecidas (ex: adaptação para jogadores de basquete).
        7. Certifique-se de que a resposta seja respeitosa, sem qualquer forma de linguagem inadequada.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
        }
    )

    response = json.loads(response.text)
    return response




@app.route('/')
def home():
    return 'API está funcionando!'

# Rota padrão JSON
@app.route('/gerar_treino', methods=['POST'])
def gerar_treino():
    try:
        dados = request.get_json()
        if not dados or not isinstance(dados, dict):
            return jsonify({'error': 'Requisição JSON inválida. Esperava um dicionário.'}), 400

        objetivo = dados.get('objetivo')
        nivel = dados.get('nivel')
        acesso_equipamentos = dados.get('acesso_equipamentos')
        restricoes = dados.get('restricoes', None)
        especificacao_treino = dados.get('especificacao_treino', "")

        if not objetivo or not nivel or not acesso_equipamentos:
            return jsonify({'error': 'Campos obrigatórios ausentes.'}), 400

        treino = criar_treino(objetivo, nivel, acesso_equipamentos, restricoes, especificacao_treino)
        return jsonify(treino), 200

    except Exception as e:
        print(f"Erro ao gerar treino: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/baixar_treino', methods=['POST'])
def baixar_treino():
    try:
        dados = request.get_json()
        
        # Extrair as partes do seu JSON
        avisos = dados.get('avisos_importantes', [])
        plano = dados.get('plano_markdown', '')
        sugestoes = dados.get('sugestoes_adicionais', '')

        # Criar o objeto PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Define as margens explicitamente (em mm)
        pdf.set_left_margin(15)
        pdf.set_right_margin(15)
        
        # Calcula a largura útil da página (Largura total - margens)
        largura_util = pdf.w - pdf.l_margin - pdf.r_margin

        # Função para limpar e imprimir
        def adicionar_paragrafo(titulo, texto, fonte_tamanho=10, negrito=False):
            if titulo:
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(largura_util, 10, txt=titulo, ln=True)
            
            estilo = 'B' if negrito else ''
            pdf.set_font("Arial", estilo, fonte_tamanho)
            
            # O truque está aqui: passamos largura_util em vez de 0
            # e garantimos que o texto não tem tabs (\t) que quebram o layout
            texto_formatado = str(texto).replace('\t', '    ').replace('#', '').replace('*', '')
            texto_final = texto_formatado.encode('latin-1', 'replace').decode('latin-1')
            
            pdf.multi_cell(largura_util, 7, txt=texto_final)
            pdf.ln(5)

        # 1. Título Principal
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(largura_util, 10, txt="TreinAI - Seu Plano Personalizado", ln=True, align='C')
        pdf.ln(10)

        # 2. Adicionar as seções usando a função segura
        if avisos:
            adicionar_paragrafo("AVISOS IMPORTANTES", "\n".join(avisos), negrito=True)
        
        if plano:
            adicionar_paragrafo("PLANO DE TREINO", plano)
            
        if sugestoes:
            adicionar_paragrafo("SUGESTÕES ADICIONAIS", sugestoes)

        # Gerar o arquivo para download
        pdf_output = io.BytesIO()
        pdf_bytes = pdf.output() # No fpdf2, output() sem argumentos retorna os bytes
        pdf_output.write(pdf_bytes)
        pdf_output.seek(0)

        return send_file(
            pdf_output,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='meu_treino_treinai.pdf'
        )

    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
