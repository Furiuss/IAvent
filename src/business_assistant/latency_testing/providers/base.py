from abc import ABC, abstractmethod
from typing import Dict, Any


class LLMProvider(ABC):
    """Classe abstrata base para provedores de LLM"""

    @abstractmethod
    def initialize(self, **kwargs) -> None:
        """Inicializa o cliente do provedor com as credenciais necessárias"""
        pass

    @abstractmethod
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Faz uma requisição para o modelo e retorna a resposta"""
        pass

    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o modelo sendo usado"""
        pass