from abc import abstractmethod
from typing import Dict, Any, Optional
from ..core.base import AssistantBase
from ..core.hydbrid_knowledge import HybridKnowledgeBase


class BaseAssistantProvider(AssistantBase):
    """Classe base para providers específicos."""

    def __init__(self,
                 knowledge_base: HybridKnowledgeBase,
                 model_config: Dict[str, Any]):
        super().__init__(knowledge_base)
        self.model_config = model_config
        self.conversation_history = []

    @abstractmethod
    async def prepare_prompt(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Prepara o prompt com base na mensagem e contexto."""
        pass