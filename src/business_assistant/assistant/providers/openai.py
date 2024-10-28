from typing import Dict, Any, Optional
from openai import AsyncOpenAI
from .base import BaseAssistantProvider
from ..core.knowledge import KnowledgeBase
from ..utils.context import ContextManager


class OpenAIAssistant(BaseAssistantProvider):
    """Implementação do assistente usando GPT (OpenAI)."""

    def __init__(self,
                 knowledge_base: KnowledgeBase,
                 api_key: str,
                 model: str = "gpt-4-turbo-preview"):
        super().__init__(knowledge_base, {
            "model": model,
            "api_key": api_key
        })
        self.client = AsyncOpenAI(api_key=api_key)
        self.context_manager = ContextManager()

    async def prepare_prompt(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        context_info = ""
        if context:
            context_info = f"Previous context: {context}\n\n"

        kb_info = self.knowledge_base.get_relevant_info(message)
        return f"{context_info}Knowledge base information: {kb_info}\n\nUser message: {message}"

    async def chat(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        prompt = await self.prepare_prompt(message, context)

        response = await self.client.chat.completions.create(
            model=self.model_config["model"],
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    async def load_context(self, context_id: str) -> Dict[str, Any]:
        """Carrega o contexto da conversa."""
        context = await self.context_manager.load(context_id)
        return context if context else {}

    async def save_context(self, context_id: str, context: Dict[str, Any]) -> None:
        """Salva o contexto da conversa."""
        await self.context_manager.save(context_id, context)