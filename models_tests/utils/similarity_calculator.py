from typing import List
import numpy as np
from anthropic import Anthropic

class SimilarityCalculator:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)

    def get_embedding(self, text: str) -> List[float]:
        response = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            system="Retorne apenas o embedding do texto fornecido, sem explicações.",
            messages=[{"role": "user", "content": text}]
        )
        return response.content[0].text

    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def calcular_similaridade(self, texto1: str, texto2: str) -> float:
        embedding1 = self.get_embedding(texto1)
        embedding2 = self.get_embedding(texto2)
        return self.cosine_similarity(embedding1, embedding2)


def exemplo_uso():
    calculator = SimilarityCalculator("seu-api-key-aqui")

    texto1 = "O gato está dormindo no sofá"
    texto2 = "Um felino descansa no mobiliário"

    similaridade = calculator.calcular_similaridade(texto1, texto2)
    print(f"Similaridade entre os textos: {similaridade:.2f}")