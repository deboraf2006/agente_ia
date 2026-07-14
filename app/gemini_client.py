import time
import requests
from flask import current_app

def obter_resposta_do_gemini(prompt_texto, max_tentativas=3):
    """
    Envia um prompt para o Gemini, com retentativas em caso de erro 429/503.
    """
    url = current_app.config['API_URL']
    api_key = current_app.config['GEMINI_API_KEY']

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY não configurada. Verifique o arquivo .env")

    headers = {'Content-Type': 'application/json'}
    params = {'key': api_key}
    payload = {
        'contents': [
            {
                'parts': [
                    {'text': prompt_texto}
                ]
            }
        ]
    }

    for tentativa in range(1, max_tentativas + 1):
        response = requests.post(url, headers=headers, params=params, json=payload)

        if response.status_code == 200:
            dados = response.json()
            try:
                return dados['candidates'][0]['content']['parts'][0]['text']
            except (KeyError, IndexError) as e:
                raise ValueError(f"Resposta do Gemini em formato inesperado: {dados}") from e

        # Se for erro de limite de requisições ou serviço indisponível, espera e tenta de novo
        if response.status_code in (429, 503):
            if tentativa == max_tentativas:
                raise RuntimeError(f"Serviço do Gemini indisponível após {max_tentativas} tentativas (erro {response.status_code}).")
            espera = 2 ** tentativa  # 2, 4, 8 segundos
            print(f"⏳ Tentativa {tentativa} falhou com {response.status_code}. Aguardando {espera}s...")
            time.sleep(espera)
            continue

        # Outros erros (ex.: 403, 400) são levantados imediatamente
        response.raise_for_status()

    # Se o loop terminar sem retornar, erro inesperado
    raise RuntimeError("Erro inesperado ao chamar a API do Gemini.")