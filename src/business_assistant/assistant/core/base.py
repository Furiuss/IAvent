from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class AssistantBase(ABC):
    """Classe base abstrata para implementações de assistentes."""

    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base

    @abstractmethod
    async def chat(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Processa uma mensagem e retorna a resposta."""
        pass

    @abstractmethod
    async def load_context(self, context_id: str) -> Dict[str, Any]:
        """Carrega o contexto de uma conversa."""
        pass

    @abstractmethod
    async def save_context(self, context_id: str, context: Dict[str, Any]) -> None:
        """Salva o contexto de uma conversa."""
        pass
