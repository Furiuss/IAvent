from typing import Dict, Any, Optional
import anthropic
from .base import BaseAssistantProvider
from ..core.hydbrid_knowledge import HybridKnowledgeBase
from ..utils.context import ContextManager


class AnthropicAssistant(BaseAssistantProvider):
    """Implementação do assistente usando Claude (Anthropic)."""

    def __init__(self,
                 knowledge_base: HybridKnowledgeBase,
                 api_key: str,
                 model: str = "claude-3-opus-20240229"):
        super().__init__(knowledge_base, {
            "model": model,
            "api_key": api_key
        })
        self.client = anthropic.Client(api_key=api_key)
        self.context_manager = ContextManager()

    async def prepare_prompt(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        context_info = ""
        if context:
            context_info = f"Previous context: {context}\n\n"

        kb_info = self.knowledge_base.get_info(message)

        if kb_info["mode_used"] == 'api':
            return kb_info["results"]

        return f"{context_info}Knowledge base information: {kb_info}\n\nUser message: {message}"

    async def chat(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        prompt = await self.prepare_prompt(message, context)
        return prompt['response']
        # response = await self.client.messages.create(
        #     model=self.model_config["model"],
        #     messages=[{"role": "user", "content": prompt}]
        # )
        #
        # return response.content[0].text

    async def load_context(self, context_id: str) -> Dict[str, Any]:
        """Carrega o contexto da conversa."""
        context = await self.context_manager.load(context_id)
        return context if context else {}

    async def save_context(self, context_id: str, context: Dict[str, Any]) -> None:
        """Salva o contexto da conversa."""
        await self.context_manager.save(context_id, context)