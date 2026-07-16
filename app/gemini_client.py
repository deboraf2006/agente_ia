import time
from flask import current_app
from app.agent import ChatAgent

# --- Comentário meu: Inicializa o nosso agente híbrido (ML local + Gemini) ---
agente_inteligente = ChatAgent()

def obter_resposta_do_gemini(prompt_texto, max_tentativas=3):
    """
    Envia um prompt para o Gemini usando nosso agente moderno,
    mantendo o sistema de retentativas caso a API falhe.
    """
    # Verificação de segurança que seu amigo fez
    api_key = current_app.config['GEMINI_API_KEY']
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY não configurada. Verifique o arquivo .env")

    for tentativa in range(1, max_tentativas + 1):
        try:
            # --- Comentário meu: Envia o texto para o nosso agente inteligente ---
            resposta_texto, intencao_detectada = agente_inteligente.send_message(prompt_texto)
            
            # Mostra no terminal para acompanharmos o Machine Learning funcionando
            print(f"\n[ML Web] Intenção detectada localmente: {intencao_detectada}")
            
            # Retorna a resposta limpa gerada pelo agente
            return resposta_texto

        except Exception as e:
            # Se a chamada falhar (por rede ou limite de requisições), usa o sistema de espera do seu amigo
            if tentativa == max_tentativas:
                raise RuntimeError(f"Ocorreu um erro no Agente Gemini após {max_tentativas} tentativas: {e}")
            
            espera = 2 ** tentativa  # 2, 4 segundos...
            print(f"⏳ Tentativa {tentativa} falhou. Erro: {e}. Aguardando {espera}s...")
            time.sleep(espera)

    raise RuntimeError("Erro inesperado ao chamar a API do Gemini.")