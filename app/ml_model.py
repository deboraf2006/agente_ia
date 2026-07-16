#Comentário meu: Este arquivo contém o modelo de Machine Learning clássico local 


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np

class IntentClassifier:
    def __init__(self):
        # Dados simples de treino para classificar a intenção/humor do usuário
        self.training_sentences = [
            # Técnico / Ajuda com Código
            "como fazer um loop em python", "ajuda com erro no codigo", "o que e uma api", "me de um exemplo de funcao", "como programar",
            # Suporte / Reclamação
            "nao esta funcionando", "estou com um problema", "da erro toda vez", "suporte tecnico por favor", "sistema fora do ar",
            # Casual / Conversa
            "ola tudo bem", "bom dia", "como foi seu dia", "me conte uma piada", "quem e voce", "boa tarde"
        ]
        self.training_labels = [
            "TECNICO", "TECNICO", "TECNICO", "TECNICO", "TECNICO",
            "SUPORTE", "SUPORTE", "SUPORTE", "SUPORTE", "SUPORTE",
            "CASUAL", "CASUAL", "CASUAL", "CASUAL", "CASUAL", "CASUAL"
        ]
        
        self.vectorizer = TfidfVectorizer()
        self.model = LogisticRegression()
        self._train()

    def _train(self):
        # Vetoriza o texto e treina o modelo de regressão logística clássico (ML)
        X = self.vectorizer.fit_transform(self.training_sentences)
        y = np.array(self.training_labels)
        self.model.fit(X, y)

    def predict(self, text: str) -> str:
        # Preve a intenção do usuário com base no texto digitado
        X_test = self.vectorizer.transform([text.lower()])
        prediction = self.model.predict(X_test)[0]
        # Calcula a probabilidade para saber o nível de confiança
        probabilities = self.model.predict_proba(X_test)[0]
        confidence = max(probabilities)
        
        # Se a confiança for muito baixa, classifica como "GERAL"
        if confidence < 0.4:
            return "GERAL"
        return prediction