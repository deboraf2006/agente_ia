# --- Comentário meu: Este arquivo cria o Agente de IA usando o SDK do Google Gemini ---
from google import genai
from google.genai import types
from config import GEMINI_API_KEY
from .ml_model import IntentClassifier  # O ponto (.) busca o arquivo na mesma pasta

class ChatAgent:
    def __init__(self):
        # Inicializa o cliente oficial da API do Gemini usando o SDK moderno do Google
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        
        # Inicializa o classificador de Machine Learning local
        self.classifier = IntentClassifier()
        
        # Modelo recomendado para chat rápido e eficiente (Gemini 2.5 Flash)
        self.model_name = "gemini-2.5-flash"
        
        # Histórico de conversa mantido na memória da sessão do agente
        self.chat_session = self.client.chats.create(model=self.model_name)

    def send_message(self, user_message: str) -> tuple[str, str]:
        # 1. Executa o modelo local de Machine Learning para prever a intenção
        detected_intent = self.classifier.predict(user_message)
        
        # 2. Define dinamicamente o comportamento da LLM com base na intenção predita pelo ML
        system_instruction = f"Você é um assistente de IA prestativo. A intenção detectada do usuário é {detected_intent}. "
        if detected_intent == "TECNICO":
            system_instruction += "Seja muito preciso, direto e forneça exemplos de código limpos e comentados."
        elif detected_intent == "SUPORTE":
            system_instruction += "Seja extremamente paciente, empático e focado em resolver o problema do usuário passo a passo."
        else:
            system_instruction += "Mantenha um tom natural, amigável e descontraído."

        # 3. Envia a mensagem para a API do Gemini injetando o contexto do Machine Learning
        response = self.chat_session.send_message(
            user_message,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7
            )
        )
        
        return response.text, detected_intent