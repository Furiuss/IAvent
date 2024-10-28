from typing import Dict, Any, Optional


class ContextManager:
    """Gerencia o contexto das conversas do assistente."""

    def __init__(self):
        self.contexts = {}

    async def load(self, context_id: str) -> Optional[Dict[str, Any]]:
        """Carrega um contexto específico."""
        return self.contexts.get(context_id)

    async def save(self, context_id: str, context: Dict[str, Any]) -> None:
        """Salva um contexto específico."""
        self.contexts[context_id] = context

    async def clear(self, context_id: str) -> None:
        """Limpa um contexto específico."""
        if context_id in self.contexts:
            del self.contexts[context_id]