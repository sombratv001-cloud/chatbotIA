from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime
import os
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)

# --- CONFIGURAÇÃO ---
API_KEY = os.getenv("CHAVE_API_GEMINI")

MODELO = 'gemini-2.5-flash'
URL = f'https://generativelanguage.googleapis.com/v1beta/models/{MODELO}:generateContent?key={API_KEY}'

historico = []

def enviar_ia(mensagem):
    global historico
    hora = datetime.now().strftime('%H:%M')
    
    # Prompt com Logística, Preços e Resumo de Pedido
    prompt = f"""
    Você é atendente da 'Açai na Garrafa'. 
    Preços: Açaí R$ 20,00 | Milkshake R$ 18,00.
    Mixes (máx 3): Leite Ninho, creme de ninho, gotas chocolate, MMs.
    
    LOGÍSTICA:
    - Entrega: Somente até 4km de distância. Taxa fixa de R$ 5,00.
    - Pergunte sempre se é para 'Entrega' ou 'Retirada'.
    - Se for entrega, solicite o endereço completo.
    
    FUNCIONAMENTO: 18:00 às 22:30 (Seg a Sex). Hora atual: {hora}.
    - Se fechado: Peça para adiantar o pedido e avise que confirmaremos ao abrir.
    
    FINALIZAÇÃO:
    - Assim que o cliente escolher tudo, envie um RESUMO DETALHADO (Item, Mixes, Forma de Entrega, Endereço e Valor Total) para confirmação.
    - Seja curto e amigável.
    """

    historico.append({"role": "user", "parts": [{"text": mensagem}]})
    
    payload = {
        "system_instruction": {"parts": [{"text": prompt}]},
        "contents": historico
    }

    try:
        r = requests.post(URL, json=payload).json()
        texto = r['candidates'][0]['content']['parts'][0]['text']
        historico.append({"role": "model", "parts": [{"text": texto}]})
        return texto
    except:
        return "Erro de conexão. Tente novamente."

# --- ROTAS ---
@app.route('/')
def index():
    global historico
    historico = []
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def chat():
    msg = request.json.get('message')
    return jsonify({"response": enviar_ia(msg)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')