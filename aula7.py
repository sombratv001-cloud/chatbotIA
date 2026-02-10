import requests


API_KEY = 'AIzaSyCQSK7GiGFHwl0GdFfjiliBCpHY1_P-toM'
# Ajustado para gemini-1.5-flash (versão estável atual)
model = 'gemini-2.5-flash'
url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}'

# O histórico precisa da estrutura correta de 'role' e 'parts'
conversa = [{"role": "user", "parts": [{"text": "Mantenha a conversa com poucas palavras na resposta, responda com no máximo 100 palavras, sendo objetivo e mais direto"}]}]

while True:
    opcao = input('\n1 - Conversar com o Gemini\n2 - Sair\nEscolha: ')
    
    if opcao == '1':
        prompt = input('Faça sua pergunta: ')
        
        # Adiciona a pergunta ao histórico
        conversa.append({"role": "user", "parts": [{"text": prompt}]})
        
        # A chave correta é 'contents' (plural)
        payload = {"contents": conversa}
        
        # Realiza a requisição
        resposta = requests.post(url, json=payload)
        dados = resposta.json()
        
        # Extrai o texto da resposta
        resposta_gemini = dados['candidates'][0]['content']['parts'][0]['text']
        
        # Adiciona a resposta do modelo ao histórico para manter o contexto
        conversa.append({"role": "model", "parts": [{"text": resposta_gemini}]})
        
        print(f'A resposta do Gemini foi: {resposta_gemini}')
        
    elif opcao == '2':
        print('Saindo...')
        break

